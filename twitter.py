from .base import BaseScraper

class TwitterUser(object):
    """Container for the info associated w/ a Twitter user"""
    def __init__(self,screen_name,id_):
        self.screen_name = screen_name
        self.id = id_
        pass

class TwitterScraper(BaseScraper):
    def __init__(self,user_agents = None, api_auth = None):
        """Initialize the twitter scraper."""
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
        return followers
