import logging, requests, json, re, pdb
from bs4 import BeautifulSoup
from ..models import FacebookUser, FacebookPage
from ...base import ScrapingError

regex = re.compile("https:\/\/www.facebook.com\/(.*)")
regex2 = re.compile("https:\/\/www.facebook.com\/profile.php\?id=(.*)\&ref")

logger = logging.getLogger(__name__)

"""
Getting the id using the public method can get less data than ideal.

Pages dealing with alcohol cannot be retrieved via the public method.
For example: https://www.facebook.com/zeitgeistusn

The graphapi can be helpful here. Using a user access token (or perhaps even an app 
access token) we can get the id, name, and other attributes (in the same format).

"""

def get_id(graph_name):
    "Get the graph ID given a name."""
    get_response = lambda : requests.get('https://graph.facebook.com/' + graph_name)
    response = get_response()
    counter = 0
    while response.status_code == 400 and counter < 3:
        response = get_response()
        counter += 1
    id = json.loads(response.text).get('id', None)
    return int(id) if id else None

def get_name(graph_id):
    """Get the graph name given a graph ID."""
    response = requests.get('https://graph.facebook.com/' + graph_id)
    name = json.loads(response.text).get('name', None)
    return name

def get_attribute(graph_obj,attribute):
    """Get attribute of a given a graph_name or graph_id."""
    response = requests.get('https://graph.facebook.com/' + graph_obj)
    name = json.loads(response.text).get(attribute, None)
    return name

def get_attributes(graph_obj,attributes):
    """Get multiple attributes of a given a graph_name or graph_id."""
    ret_attributes = []
    response = requests.get('https://graph.facebook.com/' + graph_obj)
    data = json.loads(response.text)
    for attribute in attributes:
        ret_attributes.append(data.get(attribute, None))
    return ret_attributes

regex1 = re.compile("^https:\/\/www.facebook.com\/([^?\n]+)(?:\?ref.*)?$")
regex2 = re.compile("https:\/\/www.facebook.com\/profile.php\?id=(.*)\&(f)?ref")
regex3 = re.compile("\/groups\/(.*)\/.*")
def parse_url(url):
    # fix this via regex
    url = url.replace("?fref=pb&hc_location=profile_browser", "")
    url = url.replace("?fref=pb&hc_location=friends_tab", "")
    regex_result = regex1.findall(url)
    if not regex_result:
        regex_result = regex3.findall(url)
    if regex_result:
        username = regex_result[0]
        if username == None: raise ValueError("No username was parsed %s" % url)
        if 'pages/' in username:
            username = username.split('/')[-1]
    else: # old style user that doesn't have username, only uid
        regex_result2 = regex2.findall(url)
        if not regex_result2: raise ValueError("URL not parseable %s" % url)
        username = regex_result2[0]

    return username

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
        # pdb.set_trace()
        raise ScrapingError("Security Check")

    html = re.sub(r'(<!--)|(-->)',' ',resp.text)
    soup = BeautifulSoup(html)

    container = soup.findAll("div",["timelineFavorites"])
    if container: 
        container = container[0]
    
        for link in container.findAll('a','mediaRowItem'):
            print "link: %s" % link
            username,uid = parse_url(link['href'])
            try:
                link['class']
                # @TODO: return facebook page instead
                yield { 'link': link['href'],
                        'name': link.text,
                        'username': username,
                        'uid': uid,
                        'num_likes': get_attribute(username,'likes'),
                        'talking_about_count': get_attribute(username,'talking_about_count'),
                        'hometown': get_attribute(username,'hometown') }
            except KeyError:
                pass

        for link in container.findAll('a'):
            print "link: %s" % link
            try:
                link['class']
            except KeyError:
                try:
                    username,uid = parse_url(link['href'])
                    yield { 'link': link['href'],
                        'name': link.text,
                        'username': username,
                        'uid': uid,
                        'num_likes': get_attribute(username,'likes'),
                        'talking_about_count': get_attribute(username,'talking_about_count'),
                        'hometown': get_attribute(username,'hometown') }
                except ValueError:
                    continue
    else:
        # pdb.set_trace()
        raise ScrapingError("User %s has no likes or tight privacy settings." % username)
