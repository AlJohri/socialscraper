from ..twitter import TwitterScraper

class TestFacebookScraper(unittest.TestCase):

	username = os.getenv("FACEBOOK_USERNAME")
	password = os.getenv("FACEBOOK_PASSWORD")

	def setUp(self):
		self.scraper = FacebookScraper()
		self.scraper.add_user(username=username, password=password)

	def test_page_scraping(self):
		self.scraper.login()
		for item in self.scraper.graph_loop("al.johri", "pages-liked"):
			print item[0]

		self.assertEqual(True,True)