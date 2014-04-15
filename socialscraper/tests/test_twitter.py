import unittest, os
from ..twitter import TwitterScraper

class TestTwitterScraper(unittest.TestCase):

	def setUp(self):
		self.email = os.getenv("TWITTER_EMAIL")
		self.username = os.getenv("TWITTER_USERNAME")
		self.password = os.getenv('TWITTER_PASSWORD')

		self.test_username = "mogellner"
		self.test_userid = 2304205154
		
		self.scraper = TwitterScraper()
		self.scraper.add_user(username=self.username, password=self.password)

	def test_with_id_and_screenname(self):
		user = self.test_username
		id = self.test_userid
		followers_from_user = self.scraper.get_followers(user)
		followers_from_id = self.scraper.get_followers(id)
		self.assertEqual([f.username for f in followers_from_user].sort(),[f.username for f in followers_from_id].sort())
		for follower in self.scraper.get_followers('aljohri'):
			print follower