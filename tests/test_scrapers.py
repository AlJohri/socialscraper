import unittest, os

from ..twitter import TwitterScraper
from ..facebook import FacebookScraper

class TestTwitterScraper(unittest.TestCase):
	def setUp(self):
		self.scraper = TwitterScraper()
		self.scraper.add_user_info(os.getenv("TWITTER_USERNAME"),os.getenv("TWITTER_PASSWORD"))
		pass

	def test_with_id_and_screenname(self):
		user = os.getenv("TWITTER_TESTUSER_SCREENNAME")
		id_ = int(os.getenv("TWITTER_TESTUSER_ID"))
		followers_from_user = self.scraper.get_followers(user)
		followers_from_id = self.scraper.get_followers(id_)
		self.assertEqual([f.screen_name for f in followers_from_user].sort(),[f.screen_name for f in followers_from_id].sort())

class TestFacebookScraper(unittest.TestCase):
	def setUp(self):
		self.scraper = FacebookScraper()
		self.scraper.add_user_info(os.getenv("FACEBOOK_USERNAME"),os.getenv("FACEBOOK_PASSWORD"))

if __name__ == "__main__":
	unittest.main()