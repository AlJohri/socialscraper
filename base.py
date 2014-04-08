from mechanize import Browser
import random

class AbstractScraper(object):
    default_user_agents = set([
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Konqueror/3.0-rc4; (Konqueror/3.0-rc4; i686 Linux;;datecode)',
        'Opera/9.52 (X11; Linux i686; U; en)'
    ])

    class _Browser(Browser):
        # disable the html check to allow for XHTML
        def viewing_html(self):
            import mechanize
            mechanize.Browser.viewing_html(self)
            return True

    def __init__(self,user_agents = None):
        self._browser = AbstractScraper._Browser()
        self._browser.set_handle_robots(False)
        if user_agents:
            self.user_agents = set(user_agents)
        else:
            self.user_agents = AbstractScraper.default_user_agents
        return

    def set_user_agent(self,user_agent):
        if user_agent not in self.user_agents:
            self.user_agents.add(user_agent)
        self._browser.addheaders = [('User-Agent',user_agent)]
        return

    def set_random_user_agent(self):
        self.set_user_agent(random.choice(self.user_agents))