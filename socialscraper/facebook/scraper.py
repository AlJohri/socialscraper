import requests, pickle, os
from requests.adapters import HTTPAdapter
from facebook import GraphAPI, GraphAPIError
from ..base import BaseScraper, BaseUser, ScrapingError

from . import auth
from . import public
from . import nograph
from . import graphapi
from . import graphsearch

FACEBOOK_MOBILE_URL = 'https://m.facebook.com'
FACEBOOK_USER_TOKEN = os.getenv('FACEBOOK_USER_TOKEN')

class FacebookUser(BaseUser):
    """Container for the info associated w/ a Facebook user"""
    def __init__(self, username=None, id=None):
        super(FacebookUser, self).__init__(id=id, username=username)

class FacebookScraper(BaseScraper):

    def __init__(self,user_agents=None, pickled_session=None, scraper_type="graphapi"):
        """Initialize the Facebook scraper."""
        if pickled_session: self.browser = pickle.loads(pickled_session)
        else:  self.browser = requests.Session()
        # TODO: write method to just pickle the whole FacebookScraper instead
        BaseScraper.__init__(self, user_agents)
        self.browser.headers = { 'User-Agent': self.cur_user_agent }
        self.browser.mount(FACEBOOK_MOBILE_URL, HTTPAdapter(pool_connections=500, pool_maxsize=500, max_retries=3))

    def init_api(self):
        self.api = GraphAPI(FACEBOOK_USER_TOKEN)

        try:
            profile = self.api.get_object('me')
        except GraphAPIError:
            self.api = None

        return bool(self.api)

    def login(self):
        """Logs user into facebook."""
        self.cur_user = self.pick_random_user()
        self.cur_user.username = auth.login(self.browser, self.cur_user.email, self.cur_user.password)
        self.cur_user.id = self.get_graph_id(self.cur_user.username)

    def logout(self):
        auth.logout(self.browser)
        self.cur_user = None

    def login_required(func):
        def _login_required(*args):
            if args[0].cur_user == None:
                raise ScrapingError("Cannot use method %s without logging in." % func)
            ret = func(*args)
            return ret
        return _login_required

    def api_required(func):
        def _api_requred(*args):
            if args[0].api == None:
                raise ScrapingError("Cannot use method %s without a valid FACEBOOK_USER_TOKEN or initializing the api." % func)
            ret = func(*args)
            return ret
        return _api_requred

    def get_graph_id(self, graph_name):
        return public.get_id(graph_name)

    def get_graph_name(self, graph_id):
        return public.get_name(graph_id)

    def get_graph_attribute(self, graph_id, attribute):
        return public.get_attribute(graph_id,attribute)

    # wrapper methods

    def get_about(self, graph_name, graph_id=None):
        if self.scraper_type == "graphapi": return self.get_about_api(graph_name)
        elif self.scraper_type == "nograph": return self.get_about_nograph(graph_name, graph_id)

    def get_feed(self, graph_name, graph_id=None):
        if self.scraper_type == "api": return self.get_feed_api(graph_name)
        elif self.scraper_type == "nograph": return self.get_feed_nograph(graph_name, graph_id)

    # graphapi

    @api_required
    def get_feed_api(self, graph_name):
        return graphapi.get_feed(self.api, graph_name)

    @api_required
    def get_about_api(self, graph_name):
        return graphapi.get_about(self.api, graph_name)

    @api_required
    def get_likes_api(self, graph_name):
        return graphapi.get_likes(self.api, graph_name)

    # nograph

    @login_required
    def get_feed_nograph(self, graph_name, graph_id=None):
        return nograph.get_feed(self.browser, self.cur_user, graph_name, graph_id=graph_id)

    @login_required
    def get_about_nograph(self, graph_name, graph_id=None):
        return nograph.get_about(self.browser, self.cur_user, graph_name, graph_id=graph_id)

    # graphsearch

    @login_required
    def graph_search(self, graph_name, method_name, graph_id=None):
        for result in graphsearch.search(self.browser, self.cur_user, graph_name, method_name, graph_id=graph_id): yield result

    # for result in self.graph_search(page_name,"likers"): yield result
    # for result in self.graph_search(user_name,"pages-liked"): yield result
    # for result in public.get_pages_liked_nograph(user_name): yield result
