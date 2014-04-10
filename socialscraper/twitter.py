from .base import BaseScraper, UsageError
import requests, json, bs4

class TwitterUser(object):
    """Container for the info associated w/ a Twitter user"""
    def __init__(self, screen_name = None, id_ = None):
        self.screen_name = screen_name
        self.id = id_

    def __str__(self):
        return "%s (%i)" % (self.screen_name, self.id)
    def __repr__(self):
        return "%s (%i)" % (self.screen_name, self.id)

class Tweet(object):
    """Container for a tweet on a timeline."""
    def __init__(self, id_, content):
        pass

class TwitterScraper(BaseScraper):
    def __init__(self,user_agents = None):
        """Initialize the twitter scraper."""
        BaseScraper.__init__(self,user_agents)

    def get_feed_by_screen_name(self,screen_name):
        """Get a twitter user's feed given their screen name."""
        user = TwitterUser(screen_name,self.id_from_screen_name(screen_name))
        cursor = str(999999999999999999)
        tweets = []

        while True:
            tweet_json = self._get_json("tweets",user.screen_name,cursor)

            html = tweet_json["items_html"]
            soup = bs4.BeautifulSoup(html)
            text_containers = soup.findAll("p","js-tweet-text")
            timestamp_containers = soup.findAll("span","_timestamp")
            for container in zip(timestamp_containers,text_containers):
                cur_tweet = Tweet(container[0]["data-time"],
                                  container[1].text.encode('utf-8','ignore'))
                tweets.append(cur_tweet)

            if not tweet_json["has_more_items"]:
                break

            cursor = tweet_json["max_id"]
        return tweets

    def get_feed_by_id(self,id_):
        """Get a user's twitter feed given their user ID."""
        return self.get_feed_by_screen_name(self.screen_name_from_id(int(id_)))

    def get_followers(self,id_or_username,max=-1):
        """Get a twitter user's feed given their numeric ID or 
        username. Type checking is used to determine the category of 
        the input argument - an ``int`` is interpreted as a numeric ID,
        while a ``string`` is interpreted as a username. 
        If max is a positive number, get_followers will only retrieve 
        up to that number of followers (note that the actual number
        returned may be slightly larger due to the parsing mechanics.)
        """

        # Determine whether the input argument is a numeric ID or a username
        user = TwitterUser()

        if (type(id_or_username) == int) or (type(id_or_username) == float):
            # ... if it's an ID, get the corresponding username
            user.id = id_or_username
            user.screen_name = self.screen_name_from_id(user.id)
        else:
            user.screen_name = id_or_username
            user.id = self.id_from_screen_name(user.screen_name)

        cursor = None

        while True:
            follower_json = self._get_json("followers",user.screen_name,cursor)
            
            # parse follower json
            html = follower_json["items_html"]
            soup = bs4.BeautifulSoup(html)
            user_containers = soup.findAll("div",["js-actionable-user",
                                                  "js-profile-popup-actionable",
                                                  "account"])
            for container in user_containers:
                cur_user = TwitterUser(container['data-screen-name']
                                        .encode('utf-8','ignore'),
                                   int(container['data-user-id']
                                        .encode('utf-8','ignore')))
                yield cur_user

            if not follower_json["has_more_items"]:
                break

            cursor = follower_json["cursor"]

    def screen_name_from_id(self,user_id):
        """Get a user's screen name from their ID."""
        url = "https://twitter.com/account/redirect_by_id/%i" % user_id
        resp = requests.request("GET", url, allow_redirects=False)
        screen_name = resp.headers['location'].split('/')[-1]

        return screen_name


    def id_from_screen_name(self,screen_name):
        """Get a user's ID from their screen name."""
        # @TODO: need to investigate if this is scalable
        url = "http://mytwitterid.com/api.php?screen_name=%s" % screen_name
        resp = requests.get(url)

        return json.loads(resp.text)[0]["user"]["id"]

    def _get_json(self, type_, screen_name, cursor):

        """Internal method to get the JSON response for a particular 
        twitter request (eg. followers or tweets.)
        """
        if type_ == "followers":
            base_url = "https://twitter.com/%s/followers/users?" % screen_name
        elif type_ == "tweets":
            base_url = "?"
            raise NotImplementedError
        else:
            raise UsageError()
        
        if cursor and type_ == "followers":
            base_url += "&cursor=" + str(cursor)
        elif cursor and type_ == "tweets":
            base_url += "&max_id=" + str()

        resp = self._browser.open(base_url)
        if "redirect_after_login" in resp.geturl():
            # login first
            self.login()
            resp = self._browser.submit()
            
        return json.loads(resp.read())

    def login(self):
        user_acct = self.pick_random_user()
        self._browser.select_form(nr=1)
        self._browser.form["session[username_or_email]"] = user_acct.username
        self._browser.form["session[password]"] = user_acct.password
