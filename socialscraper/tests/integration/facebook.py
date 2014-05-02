import unittest, os, pprint, logging
from ...facebook import FacebookScraper

logging.basicConfig(level=logging.WARN)
pp = pprint.PrettyPrinter(indent=4)

class TestFacebookScraper(unittest.TestCase):

    def setUp(self):
        self.email = os.getenv("FACEBOOK_EMAIL")
        self.username = os.getenv("FACEBOOK_USERNAME")
        self.password = os.getenv("FACEBOOK_PASSWORD")
        self.app_token = os.getenv('FACEBOOK_APP_TOKEN')
        self.user_token = os.getenv('FACEBOOK_USER_TOKEN')

        self.test_username = "todd.warren.seattle"
        self.test_pagename = "mightynest"

        self.scraper = FacebookScraper()

    def test_graphapi(self):
        self.scraper.init_api()
        # print self.scraper.get_about_api(self.test_username)
        # self.scraper.get_feed_api(self.test_username)
        pp.pprint(self.scraper.get_likes_api(self.test_username))

    def test_graphsearch(self):

        def init_graphsearch():
            self.scraper.add_user(email=self.email, password=self.password)
            self.scraper.login()

        def test_pages_liked(username):
            for item in self.scraper.graph_search(username, "pages-liked"):
                print item

        def test_likers(pagename):
            for item in self.scraper.graph_search(pagename, "likers"):
                print item

        # init_graphsearch()
        # test_pages_liked(self.test_username)
        # test_likers(self.test_pagename)

if __name__ == "__main__":
    unittest.main()