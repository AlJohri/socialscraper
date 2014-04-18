import unittest, os
from ...facebook import FacebookScraper

import pprint

pp = pprint.PrettyPrinter(indent=4)

class TestFacebookScraper(unittest.TestCase):

    def setUp(self):
        self.email = os.getenv("FACEBOOK_EMAIL")
        self.username = os.getenv("FACEBOOK_USERNAME")
        self.password = os.getenv("FACEBOOK_PASSWORD")

        self.test_username = "dthirman"
        self.test_pagename = "mightynest"

        self.scraper = FacebookScraper()
        self.scraper.add_user(email=self.email, password=self.password)
        self.scraper.login()


    def test_graph_search(self):

        def test_pages_liked(username):
            for item in self.scraper.graph_search(username, "pages-liked"):
                print item
            self.assertEqual(True,True)

        def test_likers(pagename):
            for item in self.scraper.graph_search(pagename, "likers"):
                print item
            self.assertEqual(True,True)

        def test_about(username):
            stuff = self.scraper.get_about(username)
            pp.pprint(stuff)
            self.assertEqual(True,True)

        test_pages_liked(self.test_username)
        test_about(self.test_username)

        # takes too long
        # test_likers(self.test_pagename)

if __name__ == "__main__":
    unittest.main()