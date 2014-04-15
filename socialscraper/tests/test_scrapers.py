import unittest, os, env

from ..twitter import TwitterScraper
from ..facebook import FacebookScraper

env.set_envs()

class TestTwitterScraper(unittest.TestCase):
	def setUp(self):
		self.scraper = TwitterScraper()
		self.scraper.add_user(username=os.getenv("TWITTER_USERNAME"), password=os.getenv('TWITTER_PASSWORD'))
		pass

	def test_with_id_and_screenname(self):
		user = os.getenv("TWITTER_TESTUSER_SCREENNAME")
		id_ = int(os.getenv("TWITTER_TESTUSER_ID"))
		followers_from_user = self.scraper.get_followers(user)
		followers_from_id = self.scraper.get_followers(id_)
		self.assertEqual([f.screen_name for f in followers_from_user].sort(),[f.screen_name for f in followers_from_id].sort())
		for follower in self.scraper.get_followers('aljohri'):
			print follower

class TestFacebookScraper(unittest.TestCase):
	def setUp(self):
		self.scraper = FacebookScraper()
		self.scraper.add_user(username=os.getenv("FACEBOOK_USERNAME"), password=os.getenv("FACEBOOK_PASSWORD"))

	def test_page_scraping(self):
		self.scraper.login()
		for item in self.scraper.graph_loop("al.johri","pages-liked"):
			print item[0]

		self.assertEqual(True,True)

if __name__ == "__main__":
	unittest.main()