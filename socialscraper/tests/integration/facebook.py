import unittest, os, pprint, logging, pickle
from ...facebook import FacebookScraper

logging.basicConfig(level=logging.DEBUG)
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

        self.scraper_type = "nograph"

        if not os.path.isfile('facebook_scraper.pickle'):
           self.scraper = FacebookScraper(scraper_type=self.scraper_type)
           self.scraper.add_user(email=os.getenv('FACEBOOK_EMAIL'), password=os.getenv('FACEBOOK_PASSWORD'))
           self.scraper.login()
           pickle.dump(self.scraper, open('facebook_scraper.pickle', 'wb'))
        else:
           self.scraper = pickle.load(open('facebook_scraper.pickle', 'rb'))
           self.scraper.scraper_type = self.scraper_type

    @unittest.skip("testing skipping")
    def test_graphapi(self):
        self.scraper.init_api()
        print self.scraper.get_about_api(self.test_username)
        for page in self.scraper.get_likes_api(self.test_username):
            pp.pprint(page)

        self.scraper.get_feed_api(self.test_username)

    # @unittest.skip("testing skipping")
    def test_graphsearch_pages_liked(self):
        for item in self.scraper.graph_search(self.test_username, "pages-liked"):
            print item

    # @unittest.skip("testing skipping")
    def test_graphsearch_likers(self):
        for item in self.scraper.graph_search(self.test_pagename, "likers"):
            print item

    # @unittest.skip("testing skipping")
    def test_graphsearch_friends(self):
        for item in self.scraper.graph_search(self.test_username, "friends"):
            print item

if __name__ == "__main__":
    unittest.main()