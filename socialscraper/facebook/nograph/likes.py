import logging, requests, re, pdb
from bs4 import BeautifulSoup
from .. import public
from ..models import FacebookUser, FacebookPage
from ...base import ScrapingError

logger = logging.getLogger(__name__)

def get_pages_liked(username):
    url = "https://www.facebook.com/%s/likes" % username
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
        'Accept': 'accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'en-US,en;q=0.8,nb;q=0.6',
        'Cache-Control': 'max-age=0'
    }
    resp = requests.get(url, headers = headers)

    if "Security Check" in resp.text:
        pdb.set_trace()
        raise ScrapingError("Security Check")

    html = re.sub(r'(<!--)|(-->)',' ',resp.text)
    soup = BeautifulSoup(html)

    container = soup.findAll("div",["timelineFavorites"])
    if container: 
        container = container[0]
    
        for link in container.findAll('a','mediaRowItem'):
            print "link: %s" % link
            username,uid = public.find_page_username(link['href'])
            try:
                link['class']
                yield { 'link': link['href'],
                        'name': link.text,
                        'username': username,
                        'uid': uid,
                        'num_likes': public.get_graph_attribute(username,'likes'),
                        'talking_about_count': public.get_graph_attribute(username,'talking_about_count'),
                        'hometown': public.get_graph_attribute(username,'hometown') }
            except KeyError:
                pass

        for link in container.findAll('a'):
            print "link: %s" % link
            try:
                link['class']
            except KeyError:
                try:
                    username,uid = public.find_page_username(link['href'])
                    yield { 'link': link['href'],
                        'name': link.text,
                        'username': username,
                        'uid': uid,
                        'num_likes': public.get_graph_attribute(username,'likes'),
                        'talking_about_count': public.get_graph_attribute(username,'talking_about_count'),
                        'hometown': public.get_graph_attribute(username,'hometown') }
                except ValueError:
                    continue
    else:
        pdb.set_trace()
        print "User %s has no likes or tight privacy settings." % username
