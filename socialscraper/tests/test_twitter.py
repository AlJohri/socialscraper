from ..facebook import FacebookScraper

class TestTwitterScraper(unittest.TestCase):

	username = os.getenv("TWITTER_USERNAME")
	password = os.getenv('TWITTER_PASSWORD')
	TWITTER_TESTUSER_SCREENNAME = "mogellner"
	TWITTER_TESTUSER_ID = 2304205154

	def setUp(self):
		self.scraper = TwitterScraper()
		self.scraper.add_user(username=username, password=password)

	def test_with_id_and_screenname(self):
		user = TWITTER_TESTUSER_SCREENNAME
		id = TWITTER_TESTUSER_ID
		followers_from_user = self.scraper.get_followers(user)
		followers_from_id = self.scraper.get_followers(id_)
		self.assertEqual([f.screen_name for f in followers_from_user].sort(),[f.screen_name for f in followers_from_id].sort())
		for follower in self.scraper.get_followers('aljohri'):
			print follower