import unittest, os
from ...twitter import TwitterScraper

# from mock import patch 
# @mock.patch('requests.get', mock.Mock(side_effect = lambda k:{'aurl': 'a response', 'burl' : 'b response'}.get(k, 'unhandled request %s'%k) ))

class TestTwitterScraper(unittest.TestCase):

	def setUp(self):
		self.email = os.getenv("TWITTER_EMAIL")
		self.username = os.getenv("TWITTER_USERNAME")
		self.password = os.getenv('TWITTER_PASSWORD')

		self.test_username = "MaloneJena"
		self.test_userid = 2304205154
		
		self.scraper = TwitterScraper()
		self.scraper.add_user(username=self.username, password=self.password)

	def test_with_id_and_screenname(self):
		user = self.test_username
		# id = self.test_userid
		# followers_from_user = self.scraper.get_followers(user)
		# followers_from_id = self.scraper.get_followers(id)
		# self.assertEqual([f.username for f in followers_from_user].sort(),[f.username for f in followers_from_id].sort())

		# for follower in self.scraper.get_followers('aljohri'):
		# 	print follower

		for tweet in self.scraper.get_feed_by_screen_name('MaloneJena'):
			print tweet

		self.assertTrue(True)

if __name__ == "__main__":
	unittest.main()