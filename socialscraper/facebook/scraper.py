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
    	self.browser.mount(auth.BASE_URL, HTTPAdapter(max_retries=3))

	def login(self):
		auth.login(self.browser, self.username, self.password)

    def get_graph_id(self, graph_name):
        """Get the graph ID given a name."""
        response = requests.get('https://graph.facebook.com/' + graph_name)
        return json.loads(response.text())['id']

    def get_graph_name(self, graph_id):
        """Get the graph name given a graph ID."""
        response = requests.get('https://graph.facebook.com/' + graph_id)
        return json.loads(response.text())['name']

    def graph_search(self, graph_id, method_name, post_data = None):
        """Graph search."""
        # initial request
        if not post_data:
            base_url = "https://www.facebook.com/search/%s/%s" % (graph_id,
                                                                  method_name)
            resp = self.browser.get(base_url)
            raw_html = resp.read()
            raw_json = self._find_script_tag_with_post_data(raw_html)
            if not raw_json:
                raise ScrapingError

        else:
            parameters = {  'data': json.dumps(post_data), 
                            '__user': self.cur_user.id, 
                            '__a': 1, 
                            '__req': 'a', 
                            '__dyn': '7n8apij35CCzpQ9UmWOGUGy1m9ACwKyaF3pqzAQ',
                            '__rev': 1106672 }

            base_url = "https://www.facebook.com/ajax/pagelet/generic.php/BrowseScrollingSetPagelet?%s" % urllib.urlencode(parameters)
            resp = self.browser.get(base_url)
            resp_json = json.loads(resp.read()[9:])
            raw_json = resp_json['jsmods']
            raw_html = resp_json['payload']

        post_data = self.parse_post_data(raw_json)
        current_results = self.parse_result(raw_html)

        return post_data, current_results

    def parse_post_data(self, raw_json):
        """Parse post data."""

        require = raw_json['require']
        data_parameter = map(lambda x: x[3][1], filter(lambda x: 
                                x[0] == "BrowseScrollingPager" and 
                                x[1] == "init", 
                                require))
        cursor_parameter = map(lambda x: x[3][0], filter(lambda x: 
                                x[0] == "BrowseScrollingPager" and 
                                x[1] == "pageletComplete", 
                                require))

        data_parameter = filter(None, data_parameter)
        cursor_parameter = filter(None, cursor_parameter)

        if data_parameter and cursor_parameter: 
            return dict(data_parameter[0].items() + 
                        cursor_parameter[0].items())
        elif data_parameter:
            return dict(data_parameter[0].items())
        elif cursor_parameter:
            return dict(cursor_parameter[0].items())
        return None

    def _find_script_tag_with_post_data(self, raw_html):
        doc = lxml.html.fromstring(raw_html)
        script_tag = filter(lambda x: x.text_content().find('cursor') != -1, 
                            doc.cssselect('script'))
        if not script_tag: 
            return None
        return json.loads(script_tag[0].text_content()[35:-2])

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