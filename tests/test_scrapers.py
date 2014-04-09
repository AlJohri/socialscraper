import unittest

from ..twitter import TwitterScraper

class TestTwitterScraper(unittest.TestCase):
	def setUp(self):
		self.scraper = TwitterScraper()
		pass

	def test_get_followers(self):
		user = "aljohri"
		user_followers = []
		followers = self.scraper.get_followers(user)
		
		self.assertEqual([f.screen_name for f in followers].sort(),user_followers.sort())

	def test_with_id_and_screenname(self):
		user = "aljohri"
		id_ = 101401061
		followers_from_user = self.scraper.get_followers(user)
		followers_from_id = self.scraper.get_followers(id_)
		self.assertEqual([f.screen_name for f in followers_from_user].sort(),[f.screen_name for f in followers_from_id].sort())

if __name__ == "__main__":
	unittest.main()