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

        def test_pages_liked(username):
            for item in self.scraper.graph_search(username, "pages-liked"):
                print item
            self.assertEqual(True,True)

        def test_likers(pagename):
            for item in self.scraper.graph_search(pagename, "likers"):
                print item
            self.assertEqual(True,True)

        # def test

        def test_about(username):
            from ...facebook import about
            about.search(self.scraper.browser, self.scraper.cur_user, username)

        # test_pages_liked(self.test_username)
        # test_likers(self.test_pagename)
        test_about('moritz.gellner')
        test_about('carson.potter.3')

if __name__ == "__main__":
    unittest.main()