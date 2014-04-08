from .base import BaseScraper

class TwitterScraper(BaseScraper):
	def __init__(self,user_agents = None):
		BaseScraper.__init__(self,user_agents)
		pass

	def get_feed_by_username(self,username):
		pass

	def get_feed_by_id(self,id_):
		pass

	def get_feeds(self,list_of_users):
		pass

	def get_followers(self,id_or_username):
		pass