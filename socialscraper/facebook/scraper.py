from ..base import BaseScraper, BaseUser, UsageError, ScrapingError
import requests
from requests.adapters import HTTPAdapter

from . import auth
from . import graph
from . import about

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
        self.cur_user.username = auth.login(self.browser, self.cur_user.email, self.cur_user.password)
        self.cur_user.id = self.get_graph_id(self.cur_user.username)

    def get_graph_id(self, graph_name):
        return graph.get_id(graph_name)

    def get_graph_name(self, graph_id):
        return graph.get_name(graph_id)

    def get_about(self, graph_name):
        return about.search(self.browser, self.cur_user, graph_name)

    def graph_search(self, graph_name, method_name):
        """Graph Search Wrapper."""
        for result in graph.search(self.browser, self.cur_user, graph_name, method_name): yield result

    def get_pages_liked_by(self, user_name):
        """Graph Search Alias - pages-liked."""
        for result in self.graph_search(user_name,"pages-liked"): yield result

    def get_likers_of_page(self, page_name):
        """Graph Search Alias - likers."""
        for result in self.graph_search(page_name,"likers"): yield result

