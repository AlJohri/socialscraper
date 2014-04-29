from ..base import BaseScraper, BaseUser, UsageError, ScrapingError
import requests, pickle, re
from requests.adapters import HTTPAdapter

from bs4 import BeautifulSoup

from . import auth
from . import graph
from . import about

import pdb

regex = re.compile("https:\/\/www.facebook.com\/(.*)")
regex2 = re.compile("https:\/\/www.facebook.com\/profile.php\?id=(.*)\&ref")

class FacebookUser(BaseUser):
    """Container for the info associated w/ a Facebook user"""
    def __init__(self, username=None, id=None):
        super(FacebookUser, self).__init__(id=id, username=username)

class FacebookScraper(BaseScraper):

    def __init__(self,user_agents=None, pickled_session=None):
        """Initialize the Facebook scraper."""
        BaseScraper.__init__(self,user_agents)
        if pickled_session:
            self.browser = pickle.loads(pickled_session)
        else: 
            self.browser = requests.Session()
        self.browser.headers = { 'User-Agent': self.cur_user_agent }
        self.browser.mount(auth.BASE_URL, HTTPAdapter(pool_connections=500, pool_maxsize=500, max_retries=3))

    def login(self):
        """Logs user into facebook."""
        self.cur_user = self.pick_random_user()
        self.cur_user.username = auth.login(self.browser, self.cur_user.email, self.cur_user.password)
        self.cur_user.id = self.get_graph_id(self.cur_user.username)

    def logout(self):
        requests.post('http://www.facebook.com/logout.php')
        print "Logged out."
        return

    def get_graph_id(self, graph_name):
        return graph.get_id(graph_name)

    def get_graph_name(self, graph_id):
        return graph.get_name(graph_id)

    def get_graph_attribute(self, graph_id, attribute):
        return graph.get_attribute(graph_id,attribute)

    def get_about(self, graph_name, graph_id=None):
        return about.get(self.browser, self.cur_user, graph_name, graph_id=graph_id)

    def graph_search(self, graph_name, method_name, graph_id=None):
        print "graph name: %s" % graph_name
        print "method_name: %s" % method_name
        """Graph Search Wrapper."""
        for result in graph.search(self.browser, self.cur_user, graph_name, method_name, graph_id=graph_id): yield result

    def _find_page_username(self, url):
        regex_result = regex.findall(url)

        if regex_result:
            username = regex_result[0]
            if 'pages/' in username:
                uid = username.split('/')[-1]
                username = uid
                return username, uid

            if username == None: raise ValueError("No username was parsed %s" % url)
            uid = self.get_graph_id(username)
            # pages/The-Talking-Heads/110857288936141
            if uid == None: raise ValueError("No userid was parsed %s" % username) # just added this
            # it errors out when it HAS username but no uid (didn't think this was possible)
        else: # old style user that doesn't have username, only uid
<<<<<<< HEAD
            try:
                regex_result = regex2.findall(url)
                uid = regex_result[0]
                username = regex_result[0]
                if uid == None: raise ValueError("No userid was parsed %s" % url)
            except IndexError:
                pdb.set_trace()
=======
            # try:
            regex_result = regex2.findall(url)
            if not regex_result:
                raise ValueError("URL not parseable")
            uid = regex_result[0]
            username = regex_result[0]
            if uid == None: raise ValueError("No userid was parsed %s" % url)
            # except IndexError:
            #     import pdb
                # pdb.set_trace()
>>>>>>> 4d4ce79c80fb6e54c2a9f57938805ead392c4e59
        return username,uid

    def _get_pages_liked_nograph(self, username):
        url = "https://www.facebook.com/%s/likes" % username
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
            'Accept': 'accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'en-US,en;q=0.8,nb;q=0.6',
            'Cache-Control': 'max-age=0'
        }
        resp = requests.get(url, headers = headers)

        if "Security Check" in resp.text:
            pdb.set_trace()
            raise ScrapingError("Security Check")

        html = re.sub(r'(<!--)|(-->)',' ',resp.text)
        soup = BeautifulSoup(html)

        container = soup.findAll("div",["timelineFavorites"])
        if container: 
            container = container[0]
        
            for link in container.findAll('a','mediaRowItem'):
                print "link: %s" % link
                username,uid = self._find_page_username(link['href'])
                try:
                    link['class']
                    yield { 'link': link['href'],
                            'name': link.text,
                            'username': username,
                            'uid': uid,
                            'num_likes': self.get_graph_attribute(username,'likes'),
                            'talking_about_count': self.get_graph_attribute(username,'talking_about_count'),
                            'hometown': self.get_graph_attribute(username,'hometown') }
                except KeyError:
                    pass

            for link in container.findAll('a'):
                print "link: %s" % link
                try:
                    link['class']
                except KeyError:
                    try:
                        username,uid = self._find_page_username(link['href'])
                        yield { 'link': link['href'],
                            'name': link.text,
                            'username': username,
                            'uid': uid,
                            'num_likes': self.get_graph_attribute(username,'likes'),
                            'talking_about_count': self.get_graph_attribute(username,'talking_about_count'),
                            'hometown': self.get_graph_attribute(username,'hometown') }
                    except ValueError:
                        continue
        else:
            pdb.set_trace()
            print "User %s has no likes or tight privacy settings." % username

    def get_pages_liked_by(self, user_name, use_graph_search = False):
        """Graph Search Alias - pages-liked."""
        if use_graph_search:
            for result in self.graph_search(user_name,"pages-liked"): yield result
        else:
            for result in self._get_pages_liked_nograph(user_name):
                yield result

    def get_likers_of_page(self, page_name):
        """Graph Search Alias - likers."""
        for result in self.graph_search(page_name,"likers"): yield result

