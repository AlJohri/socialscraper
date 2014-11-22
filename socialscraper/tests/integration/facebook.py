import unittest, os, pprint, logging, pickle, itertools
from ...facebook import FacebookScraper

logging.basicConfig(level=logging.WARN)
pp = pprint.PrettyPrinter(indent=4)

def enumerate_and_run_twice(gen):
    return itertools.takewhile(lambda (i,x): i < 2, enumerate(gen))

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

    @unittest.skip("testing skipping")
    def test_graphsearch_pages_liked(self):
        gen = self.scraper.graph_search(self.test_username, "pages-liked")
        for i,item in enumerate_and_run_twice(gen):
            print item

    @unittest.skip("testing skipping")
    def test_graphsearch_likers(self):
        gen = self.scraper.graph_search(self.test_pagename, "likers")
        for i,item in enumerate_and_run_twice(gen):
            print item

    @unittest.skip("testing skipping")
    def test_graphsearch_friends(self):
        gen = self.scraper.graph_search(self.test_username, "friends")
        for i,item in enumerate_and_run_twice(gen):
            print item

    # NOT WORKING
    @unittest.skip("testing skipping")
    def test_nograph_likes(self):
        gen = self.scraper.get_likes_nograph(self.test_username)
        for i,item in enumerate_and_run_twice(gen):
            print item

    # NOT WORKING
    # @unittest.skip("testing skipping")
    def test_nograph_about(self):
        about = self.scraper.get_about_nograph(self.test_username)
        print about

if __name__ == "__main__":
    unittest.main()