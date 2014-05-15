# -*- coding: utf-8 -*-

import logging, requests, pickle, os
from requests.adapters import HTTPAdapter
from facebook import GraphAPI, GraphAPIError
from ..base import BaseScraper, ScrapingError

from . import auth
from . import public
from . import nograph
from . import graphapi
from . import graphsearch

logger = logging.getLogger(__name__)

FACEBOOK_MOBILE_URL = 'https://m.facebook.com'
FACEBOOK_USER_TOKEN = os.getenv('FACEBOOK_APP_TOKEN')

class FacebookSession(requests.sessions.Session):

    def get(self, url, **kwargs):
        response = super(FacebookSession, self).get(url, **kwargs)

        if not auth.state(response.text, auth.LOCKED) and not auth.state(response.text, auth.SECURITY_CHECK):
            return response
        else:
            raise ScrapingError("Account locked. Stop scraping!")

class FacebookScraper(BaseScraper):

    def __init__(self,user_agents=None, pickled_session=None, pickled_api=None, scraper_type="graphapi"):
        """Initialize the Facebook scraper."""
        
        self.scraper_type = scraper_type

        self.cur_user = None

        if pickled_session: self.browser = pickle.loads(pickled_session)
        else:  self.browser = FacebookSession()

        if pickled_api: self.api = pickle.loads(pickled_api)
        else: self.api = None

        # TODO: write method to just pickle the whole FacebookScraper instead

        BaseScraper.__init__(self, user_agents)
        self.browser.headers = { 'User-Agent': self.cur_user_agent }
        self.browser.mount(FACEBOOK_MOBILE_URL, HTTPAdapter(pool_connections=500, pool_maxsize=500, max_retries=3, pool_block=True))

    def init_api(self, pickled_api=None):

        if pickled_api: self.api = pickle.loads(pickled_api)
        else: self.api = GraphAPI(FACEBOOK_USER_TOKEN)

        try:
            self.api.get_object('me')
        except (GraphAPIError, AttributeError):
            raise ScrapingError("Need a valid FACEBOOK_USER_TOKEN or initializing the api.")
            self.api = None

        return bool(self.api)

    def login(self):
        """Logs user into facebook."""
        self.cur_user = self.pick_random_user()
        self.cur_user.username = auth.login(self.browser, self.cur_user.email, self.cur_user.password, username=self.cur_user.username)
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
        elif self.scraper_type == "graphsearch": raise NotImplementedError("get_about with graphsearch")

    def get_feed(self, graph_name, graph_id=None):
        if self.scraper_type == "api": return self.get_feed_api(graph_name)
        elif self.scraper_type == "nograph": return self.get_feed_nograph(graph_name, graph_id)
        elif self.scraper_type == "graphsearch": raise NotImplementedError("get_feed with graphsearch")

    def get_likes(self, graph_name, graph_id=None):
        if self.scraper_type == "api": return self.get_likes_api(graph_name)
        elif self.scraper_type == "nograph": return self.get_likes_nograph(graph_name)
        elif self.scraper_type == "graphsearch": return self.graph_search(graph_name, "pages-liked")
        elif self.scraper_type == "public": return public.get_pages_liked(graph_name)

    def get_fans(self, graph_name, graph_id=None):
        if self.scraper_type == "api": raise NotImplementedError("get_fans with graphapi")
        elif self.scraper_type == "nograph": raise NotImplementedError("get_fans with nograph")
        elif self.scraper_type == "graphsearch": return self.graph_search(graph_name, "likers")

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

    @login_required
    def get_likes_nograph(self, graph_name, graph_id=None):
        return nograph.get_likes(self.browser, self.cur_user, graph_name, graph_id=graph_id)

    # graphsearch

    @login_required
    def graph_search(self, graph_name, method_name, graph_id=None):
        for result in graphsearch.search(self.browser, self.cur_user, graph_name, method_name, graph_id=graph_id): yield result

    # for result in self.graph_search(page_name,"likers"): yield result
    # for result in self.graph_search(user_name,"pages-liked"): yield result
    # for result in public.get_pages_liked_nograph(user_name): yield result
