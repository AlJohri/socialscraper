import logging, requests, json, re, pdb
from bs4 import BeautifulSoup
from ..models import FacebookUser, FacebookPage
from ...base import ScrapingError

regex = re.compile("https:\/\/www.facebook.com\/(.*)")
regex2 = re.compile("https:\/\/www.facebook.com\/profile.php\?id=(.*)\&ref")

logger = logging.getLogger(__name__)

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

def get_attribute(graph_id,attribute):
    """Get the graph name given a graph ID."""
    response = requests.get('https://graph.facebook.com/' + graph_id)
    name = json.loads(response.text).get('attribute', None)
    return name

def find_page_username(url):

    regex_result = regex.findall(url)

    if regex_result:
        username = regex_result[0]
        if 'pages/' in username:
            uid = username.split('/')[-1]
            username = uid
            return username, uid

        if username == None: raise ValueError("No username was parsed %s" % url)
        uid = get_id(username)
        # pages/The-Talking-Heads/110857288936141
        if uid == None: raise ValueError("No userid was parsed %s" % username) # just added this
        # it errors out when it HAS username but no uid (didn't think this was possible)
    else: # old style user that doesn't have username, only uid
        regex_result = regex2.findall(url)
        if not regex_result:
            raise ValueError("URL not parseable")
        uid = regex_result[0]
        username = regex_result[0]
        if uid == None: raise ValueError("No userid was parsed %s" % url)
    return username,uid

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
            username,uid = find_page_username(link['href'])
            try:
                link['class']
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
                    username,uid = find_page_username(link['href'])
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
        pdb.set_trace()
        print "User %s has no likes or tight privacy settings." % username
