from .base import BaseScraper, RateLimitError

class TwitterScraper(BaseScraper):
	class ApiAuth(object):
		"""Container for the authentication information needed to 
		access twitter's API.
		"""

		_api_limits = {
			"get_followers_pagination": 5000
		}
		def __init__(self,consumer_key,consumer_secret,access_token_key,
					 access_token_secret):
			import twitter # don't import twitter unless we have to
			self.api_obj = twitter.Api(
				consumer_key = consumer_key,
				consumer_secret = consumer_secret,
				access_token_key = access_token_key,
				access_token_secret = access_token_secret)

	def __init__(self,user_agents = None, api_auth = None):
		"""Initialize the twitter scraper. If api_auth is supplied, it
		should be an instance of TwitterScraper.ApiAuth containing your
		access information to the twitter API. The scraper will then 
		attempt to use the API whenever it is faster to do so, and
		scrape otherwise.
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
		"""Get a twitter user's feed given their numeric ID or 
		username. Type checking is used to determine the category of 
		the input argument - an ``int`` is interpreted as a numeric ID,
		while a ``string`` is interpreted as a username. 
		"""

		# Determine whether the input argument is a numeric ID or a username
		is_id = False
		if (type(id_or_username) == int) or (type(id_or_username) == float):
			is_id = True

		# Call the appropriate internal method based on whether API auth 
		# information exists and whether the rate limit is reached.
		followers = []
		cursor = 0
		if self.api_auth:
			while True:
				try:
					f,cont = self._get_followers_api(id_or_username,
													 is_id=is_id,cursor=cursor)
				except RateLimitError:
					break
				followers += f
				if not cont:
					return followers

				# if we are continuing, then the number of followers returned
				# has to equal the pagination limit of the API - otherwise, 
				# something is wrong!

				# column length > 80, but rules are made to be broken
				pg_limit = TwitterScraper.ApiAuth._api_limits["get_followers_pagination"]
				assert len(followers) == pg_limit
				cursor += pg_limit

		followers += self._get_followers_noapi(id_or_username,is_id=is_id,
											   cursor=cursor)
		return followers
		
	def _get_followers_api(self,id_or_username,is_id,cursor=-1):
		"""Get the followers of a particular user using the stored 
		twitter API info. Returns a chunk of followers starting at the 
		given cursor position. May throw RateLimitError.
		"""
		pass # return f=[...],cont=t/f

	def _get_followers_noapi(self,id_or_username,is_id,cursor=-1):
		"""Get the followers of a particular user by scraping, starting
		at the given cursor position.
		"""
		pass # return f=[...]
