from .base import BaseScraper

class TwitterScraper(BaseScraper):
	class ApiAuth(object):
		def __init__(self,consumer_key,consumer_secret,access_token_key,access_token_secret):
			self.consumer_key = consumer_key
			self.consumer_secret = consumer_secret
			self.access_token_key = access_token_key
			self.access_token_secret = access_token_secret
			pass

	def __init__(self,user_agents = None, api_auth = None):
		"""Initialize the twitter scraper. If api_auth is supplied, it should be an instance
		of TwitterScraper.ApiAuth containing your access information to the twitter API. The scraper
		will then attempt to use the API whenever it is faster to do so, and scrape otherwise.
		"""
		self.api_auth = api_auth
		BaseScraper.__init__(self,user_agents)
		pass

	def get_feed_by_username(self,username):
		"""Get a twitter user's feed given their username."""
		pass

	def get_feed_by_id(self,id_):
		"""Get a twitter user's feed given their numeric ID."""
		pass

	def get_followers(self,id_or_username):
		"""Get a twitter user's feed given their numeric ID or username.
		Type checking is used to determine the category of the input argument - an ``int`` is interpreted
		as a numeric ID, while a string is interpreted as a username. 
		"""
		pass