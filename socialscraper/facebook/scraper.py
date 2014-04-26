from ..base import BaseScraper, BaseUser, UsageError, ScrapingError
import requests, pickle, re
from requests.adapters import HTTPAdapter

from bs4 import BeautifulSoup

from . import auth
from . import graph
from . import about

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

    def get_about(self, graph_name, graph_id=None):
        return about.get(self.browser, self.cur_user, graph_name, graph_id=graph_id)

    def graph_search(self, graph_name, method_name, graph_id=None):
        print "graph name: %s" % graph_name
        print "method_name: %s" % method_name
        """Graph Search Wrapper."""
        for result in graph.search(self.browser, self.cur_user, graph_name, method_name, graph_id=graph_id): yield result

    def _get_pages_liked_nograph(self, username):
        url = "https://www.facebook.com/%s/likes" % username
        resp = requests.get(url)
        html = re.sub(r'(<!--)|(-->)',' ',resp.text)
        soup = BeautifulSoup(html)

        container = soup.findAll("div",["timelineFavorites"])[0]
        
        for link in container.findAll('a','mediaRowItem'):
            try:
                link['class']
                yield { 'link': link['href'],
                        'name': link.text }
            except KeyError:
                pass

        for link in container.findAll('a'):
            try:
                link['class']
            except KeyError:
                yield { 'link': link['href'],
                        'name': link.text }

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

