import unittest, os
from ...facebook import FacebookScraper

class TestFacebookScraper(unittest.TestCase):

	def setUp(self):
		self.email = os.getenv("FACEBOOK_EMAIL")
		self.username = os.getenv("FACEBOOK_USERNAME")
		self.password = os.getenv("FACEBOOK_PASSWORD")

		self.test_username = "al.johri"
		self.test_pagename = "mightynest"

		self.scraper = FacebookScraper()
		self.scraper.add_user(email=self.email, password=self.password)

	def test_page_scraping(self):
		self.scraper.login()
		for item in self.scraper.graph_loop(self.test_username, "pages-liked"):
			print item

		self.assertEqual(True,True)

if __name__ == "__main__":
	unittest.main()