from ..base import BaseScraper, BaseUser, UsageError, ScrapingError
import lxml.html, re, json, urllib, requests
from requests.adapters import HTTPAdapter

from . import auth

class FacebookUser(BaseUser):
    """Container for the info associated w/ a Facebook user"""
    def __init__(self, username=None, id=None):
        super(FacebookUser, self).__init__(id=id, username=username)

class FacebookScraper(BaseScraper):

    def __init__(self,user_agents = None):
        """Initialize the Facebook scraper."""
        BaseScraper.__init__(self,user_agents)
        self.browser = requests.Session()
        self.browser.headers = { 'User-Agent': self.cur_user_agent }
        self.browser.mount(auth.BASE_URL, HTTPAdapter(max_retries=3))

    def login(self):
        """Logs user into facebook."""
        self.cur_user = self.pick_random_user()
        auth.login(self.browser, self.cur_user.email, self.cur_user.password)

        base_url = 'https://m.facebook.com/profile.php'
        response = self.browser.get(base_url)
        doc = lxml.html.fromstring(response.content)

        profile_url = doc.cssselect('.sec')[0].get('href')

        self.cur_user.username = re.sub('\?.*', '', profile_url[1:])
        self.cur_user.id = self.get_graph_id(self.cur_user.username)

    def get_graph_id(self, graph_name):
        """Get the graph ID given a name."""
        response = requests.get('https://graph.facebook.com/' + graph_name)
        return json.loads(response.text)['id']

    def get_graph_name(self, graph_id):
        """Get the graph name given a graph ID."""
        response = requests.get('https://graph.facebook.com/' + graph_id)
        return json.loads(response.text)['name']

    def graph_search(self, graph_id, method_name, post_data = None):
        """Graph search."""
        # initial request
        if not post_data:
            base_url = "https://www.facebook.com/search/%s/%s" % (graph_id,
                                                                  method_name)
            response = self.browser.get(base_url)
            raw_html = response.text
            raw_json_cursor = self._find_script_tag_with_cursor_data(raw_html)
            raw_json_other = self._find_script_tag_with_other_data(raw_html)

            cursor_data = self.parse_cursor_data(raw_json_cursor)
            other_data = self.parse_other_data(raw_json_other)

            if not cursor_data and not other_data:
                raise ScrapingError("Couldn't find post data on initial request.")

            post_data = dict(cursor_data.items() + other_data.items())

        else:

            payload = {
                'data': json.dumps(post_data), 
                '__user': self.cur_user.id, 
                '__a': 1, 
                '__req': 'a', 
                '__dyn': '7n8apij35CCzpQ9UmWOGUGy1m9ACwKyaF3pqzAQ',
                '__rev': 1106672
            }

            # base_url = "https://www.facebook.com/ajax/pagelet/generic.php/BrowseScrollingSetPagelet"
            # response = self.browser.get(base_url, data=payload)
            
            alt_url = "https://www.facebook.com/ajax/pagelet/generic.php/BrowseScrollingSetPagelet?%s" % urllib.urlencode(payload)
            response = self.browser.get(alt_url)
            
            resp_json = json.loads(response.content[9:])
            raw_json = resp_json
            raw_html = resp_json['payload']

            post_data = self.parse_cursor_data(raw_json)

        current_results = self.parse_result(raw_html)

        return post_data, current_results

    def parse_other_data(self, raw_json):
        require = raw_json['jsmods']['require']

        data_parameter = map(lambda x: x[3][1], 
                            filter(lambda x: 
                                x[0] == "BrowseScrollingPager" and 
                                x[1] == "init", 
                                require)
                            )[0]

        return data_parameter

    def parse_cursor_data(self, raw_json):
        require = raw_json['jsmods']['require']

        cursor_parameter = map(lambda x: x[3][0], 
                                filter(lambda x: 
                                    x[0] == "BrowseScrollingPager" and 
                                    x[1] == "pageletComplete", 
                                    require)
                                )[0]
        
        return cursor_parameter


    def _find_script_tag_with_cursor_data(self, raw_html):
        doc = lxml.html.fromstring(raw_html)
        script_tag = filter(lambda x: x.text_content().find('cursor') != -1, 
                            doc.cssselect('script'))
        if not script_tag: 
            return None
        return json.loads(script_tag[0].text_content()[24:-1])

    def _find_script_tag_with_other_data(self, raw_html):
        doc = lxml.html.fromstring(raw_html)
        script_tag = filter(lambda x: x.text_content().find('encoded_query') != -1, 
                            doc.cssselect('script'))
        if not script_tag: 
            return None
        return json.loads(script_tag[0].text_content()[24:-1])


    def parse_result(self, raw_html):
        doc = lxml.html.fromstring(raw_html)
        return map(lambda x: (x.get('href'), x.text_content()) , 
                    doc.cssselect('div[data-bt*=title] a'))

    def graph_loop(self,graph_name,method_name):
        graph_id = self.get_graph_id(graph_name)
        post_data, cur_results = self.graph_search(graph_id, method_name)
        if post_data == None or cur_results == None: raise ScrapingError
        for result in cur_results: yield result

        while post_data:
            cur_post_data, cur_results = \
                self.graph_search(graph_id, method_name, post_data)
            
            if cur_post_data == None or cur_results == None: break
            for result in cur_results: yield result
            post_data.update(cur_post_data)
        return

    # Wrappers for the various graph search methods
    def get_pages_liked_by(self, user_name):
        for result in self.graph_loop(user_name,"pages-liked"):
            yield result

    def get_likers_of_page(self, page_name):
        for result in self.graph_loop(page_name,"likers"):
            yield result