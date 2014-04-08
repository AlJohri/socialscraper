from .base import BaseScraper

class FacebookScraper(BaseScraper):
	def __init__(self,user_agents = None):
		BaseScraper.__init__(self,user_agents)
		pass

	def set_user_accts(self):
		pass