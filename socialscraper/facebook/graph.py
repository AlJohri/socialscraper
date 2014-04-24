import logging, requests, lxml.html, json, urllib, re
from ..base import ScrapingError
from .models import *

import pdb

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SEARCH_URL = 'https://www.facebook.com/search'
AJAX_URL = 'https://www.facebook.com/ajax/pagelet/generic.php/BrowseScrollingSetPagelet'
regex = re.compile("https:\/\/www.facebook.com\/(.*)\?ref")

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
        if not script_tag: return None
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

    def _result_to_model(result, method_name):

        regex_result = regex.findall(result[0])

        url = result[0]
        name = result[1]
        username = regex_result[0] if regex_result else None
        uid = int(get_id(graph_name))

        if method_name == "pages-liked":
            return FacebookPage(page_id=uid, username=username, url=url, name=name)
        elif method_name == "likers":
            return FacebookUser(uid=uid, username=username, url=url, name=name)
        else:
            raise ScrapingError("Wut kinda model is %. Check out da _result_to_model method" % method_name)

    # https://www.facebook.com/search/str/ruchi/users-named
    # https://www.facebook.com/search/str/ruchi/users-named/me/friends/intersect?ref=filter
    # https://www.facebook.com/search/str/ruchi/users-named/228401243342/students/intersect?ref=filter
    # https://www.facebook.com/search/str/ruchi/users-named/males/intersect?ref=filter
    # https://www.facebook.com/search/str/ruchi/users-named/females/intersect?ref=filter
    # https://www.facebook.com/search/str/ruchi/users-named/108641632493225/residents/present/intersect?ref=filter
    # https://www.facebook.com/search/str/ruchi/users-named/108659242498155/residents/present/intersect?ref=filter
    # https://www.facebook.com/search/str/ruchi/users-named/106517799384578/residents/present/intersect?ref=filter
    # https://www.facebook.com/search/str/ruchi/users-named/108007405887967/visitors/intersect
    def _graph_request(graph_id, method_name, post_data = None):
        if not post_data:
            response = browser.get(SEARCH_URL + "/%s/%s" % (graph_id, method_name))
            cursor_tag = _find_script_tag(response.text, "cursor")
            ajax_tag = _find_script_tag(response.text, "encoded_query")
            cursor_data = _parse_cursor_data(cursor_tag) if cursor_tag else None
            ajax_data = _parse_ajax_data(ajax_tag) if ajax_tag else None
            post_data = dict(cursor_data.items() + ajax_data.items()) if ajax_data and cursor_data else None

            current_results = []

            # Extract current_results from first page
            for element in lxml.html.fromstring(response.text).cssselect(".hidden_elem"): 
                comment = element.xpath("comment()")
                if not comment: continue
                element_from_comment = lxml.html.tostring(comment[0])[5:-4]
                doc = lxml.html.fromstring(element_from_comment)
                current_results += map(lambda x: (x.get('href'), x.text_content()), doc.cssselect('div[data-bt*=title] a'))
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
    for result in current_results: yield _result_to_model(result, method_name)

    while post_data:
        current_post_data, current_results = _graph_request(graph_id, method_name, post_data)
        if current_post_data == None or current_results == None: break
        for result in current_results: yield _result_to_model(result, method_name)
        post_data.update(current_post_data)
