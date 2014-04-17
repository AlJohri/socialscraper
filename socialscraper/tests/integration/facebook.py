import unittest, os
from ...facebook import FacebookScraper

import json
import urllib

class TestFacebookScraper(unittest.TestCase):

    def setUp(self):
        self.email = os.getenv("FACEBOOK_EMAIL")
        self.username = os.getenv("FACEBOOK_USERNAME")
        self.password = os.getenv("FACEBOOK_PASSWORD")

        self.test_username = "moritz.gellner"
        self.test_pagename = "mightynest"

        self.scraper = FacebookScraper()
        self.scraper.add_user(email=self.email, password=self.password)
        self.scraper.login()


    def test_graph_search(self):

        def test_pages_liked():
            for item in self.scraper.graph_search(self.test_username, "pages-liked"):
                print item
            self.assertEqual(True,True)

        def test_likers():
            for item in self.scraper.graph_search(self.test_pagename, "likers"):
                print item
            self.assertEqual(True,True)

        def test_about():
            from ...facebook import about
            about.search(self.scraper.browser, self.test_username)

        # test_pages_liked()
        # test_likers()
        test_about()

if __name__ == "__main__":
    unittest.main()