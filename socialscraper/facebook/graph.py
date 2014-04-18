import logging, requests, lxml.html, json, urllib
from ..base import ScrapingError

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SEARCH_URL = 'https://www.facebook.com/search'
AJAX_URL = 'https://www.facebook.com/ajax/pagelet/generic.php/BrowseScrollingSetPagelet'

def get_id(graph_name):
    "Get the graph ID given a name."""
    response = requests.get('https://graph.facebook.com/' + graph_name)
    return json.loads(response.text)['id']

def get_name(graph_id):
    """Get the graph name given a graph ID."""
    response = requests.get('https://graph.facebook.com/' + graph_id)
    return json.loads(response.text)['name']

def search(browser, current_user, graph_name, method_name):
    """
    
    Facebook Graph Search Generator

    General Usage:

    for result in search(browser, current_user, graph_name, method_name):
        print result

    browser: authenticated requests session (see auth.py)
    current_user: authenticated user
    graph_name: name of Facebook graph object such as a user name or page name
    method_name: name of internal Facebook graph search methods;
                 list: 'pages-liked', 'likers', 'users-named'

    Example:

    for result in search(browser, current_user, "al.johri", "pages-liked"):
        print result

    for result in search(browser, current_user, "mightynest", "likers"):
        print result

    """

    def _find_script_tag(raw_html, phrase):
        doc = lxml.html.fromstring(raw_html)
        script_tag = filter(lambda x: x.text_content().find(phrase) != -1, doc.cssselect('script'))
        if not script_tag: raise ScrapingError("Couldn't find script tag")
        return json.loads(script_tag[0].text_content()[24:-1])

    def _parse_ajax_data(raw_json):
        require = raw_json['jsmods']['require']
        tester = lambda x: x[0] == "BrowseScrollingPager" and x[1] == "init"
        data_parameter = map(lambda x: x[3][1], filter(tester, require))[0]
        return data_parameter

    def _parse_cursor_data(raw_json):
        require = raw_json['jsmods']['require']
        tester = lambda x: x[0] == "BrowseScrollingPager" and x[1] == "pageletComplete"
        cursor_parameter = map(lambda x: x[3][0], filter(tester, require))[0]
        return cursor_parameter

    def _parse_result(raw_html):
        doc = lxml.html.fromstring(raw_html)
        return map(lambda x: (x.get('href'), x.text_content()), doc.cssselect('div[data-bt*=title] a'))

    def _get_payload(ajax_data, uid):
        return {
            'data': json.dumps(ajax_data), 
            '__user': uid, 
            '__a': 1, 
            '__req': 'a', 
            '__dyn': '7n8apij35CCzpQ9UmWOGUGy1m9ACwKyaF3pqzAQ',
            '__rev': 1106672
        }

    # https://www.facebook.com/search/str/ruchi/users-named
    # https://www.facebook.com/search/str/ruchi/users-named/me/friends/intersect?ref=filter
    # https://www.facebook.com/search/str/ruchi/users-named/228401243342/students/intersect?ref=filter
    # https://www.facebook.com/search/str/ruchi/users-named/males/intersect?ref=filter
    # https://www.facebook.com/search/str/ruchi/users-named/females/intersect?ref=filter
    # https://www.facebook.com/search/str/ruchi/users-named/108641632493225/residents/present/intersect?ref=filter
    # https://www.facebook.com/search/str/ruchi/users-named/108659242498155/residents/present/intersect?ref=filter
    # https://www.facebook.com/search/str/ruchi/users-named/106517799384578/residents/present/intersect?ref=filter
    def _graph_request(graph_id, method_name, post_data = None):
        if not post_data:
            response = browser.get(SEARCH_URL + "/%s/%s" % (graph_id, method_name))
            cursor_tag = _find_script_tag(response.text, "cursor")
            ajax_tag = _find_script_tag(response.text, "encoded_query")
            cursor_data = _parse_cursor_data(cursor_tag)
            ajax_data = _parse_ajax_data(ajax_tag)
            if not ajax_data: raise ScrapingError("Couldn't find ajax post data")

            post_data = dict(cursor_data.items() + ajax_data.items())
            current_results = [] # TODO: implement getting results from first page
        else:
            payload = _get_payload(post_data, current_user.id)
            response = browser.get(AJAX_URL + "?%s" % urllib.urlencode(payload))
            raw_json = json.loads(response.content[9:])
            raw_html = raw_json['payload']
            
            post_data = _parse_cursor_data(raw_json)
            current_results = _parse_result(raw_html)
        return post_data, current_results

    # Main Facebook Graph Search

    graph_id = get_id(graph_name)
    post_data, current_results = _graph_request(graph_id, method_name)
    if post_data == None: raise ScrapingError("Coudln't find initial post data")
    for result in current_results: yield result

    while post_data:
        current_post_data, current_results = _graph_request(graph_id, method_name, post_data)
        if current_post_data == None or current_results == None: break
        for result in current_results: yield result
        post_data.update(current_post_data)
