# -*- coding: utf-8 -*-

import re, json, lxml, urllib
from bs4 import BeautifulSoup
from ...base import ScrapingError
from ..models import FacebookPage

from ..import graphapi, public

AJAX_URL = "https://www.facebook.com/ajax/pagelet/generic.php/ManualCurationOGGridCollectionPagelet"
LIKES_URL = "https://www.facebook.com/%s/%s"

# LIKES_TYPES = [
#   'likes_people', 
#   'likes_restaurants', 
#   'likes_sports', 
#   'likes_clothing', 
#   'likes_other'
# ]

def get_likes(browser, current_user, graph_name, graph_id = None, api = None):

    def _find_script_tag(raw_html, phrase):
        doc = lxml.html.fromstring(raw_html)
        script_tag = filter(lambda x: x.text_content().find(phrase) != -1, doc.cssselect('script'))
        if not script_tag: return None
        return json.loads(script_tag[0].text_content()[24:-1])

    def _parse_cursor_data(raw_json):
        if raw_json.get('error'): raise ScrapingError(raw_json.get('errorDescription'))
        require = raw_json['jsmods']['require']
        tester = lambda x: x[0] == "TimelineAppCollection" and x[1] == "enableContentLoader"
        cursor_parameter = map(lambda x: [x[3][0].replace("pagelet_timeline_app_collection_", ""), x[3][2]], filter(tester, require))
        return cursor_parameter

    def _get_payload(ajax_data, uid):
        return {
            'data': json.dumps(ajax_data), 
            '__user': uid, 
            '__a': 1, 
            '__req': 'n', 
            '__dyn': '7n8ahyj2qmumdDgDxyIJ3Ga58Ciq2W8GA8ABGeqheCu6popGiGw',
            '__rev': 1243607
        }

    def _result_to_model(result):

        url = result[0]
        name = result[1]

        username = public.parse_url(url)

        if api:
            page_id, category = graphapi.get_attributes(api, username, ["id", "category"])
        else:
            page_id, category = public.get_attributes(username, ["id", "category"])

        if page_id == None: raise ValueError("Couldn't find page_id of %s" % username)

        page_id = int(page_id)

        return FacebookPage(page_id=page_id, username=username, url=url, name=name, type=category)

    response = browser.get(LIKES_URL % (graph_name, 'likes'))
    soup = BeautifulSoup(response.content.replace('<!--','').replace('-->',''))

    CURRENT_LIKES_TYPES = []

    try:
        for x in soup.findAll('div', {'aria-role': 'tablist'})[0]: 
            if   'People' in x.text:        CURRENT_LIKES_TYPES.append('likes_people')
            elif 'Restaurants' in x.text:   CURRENT_LIKES_TYPES.append('likes_restaurants')
            elif 'Sports' in x.text:        CURRENT_LIKES_TYPES.append('likes_sports')
            elif 'Clothing' in x.text:      CURRENT_LIKES_TYPES.append('likes_clothing')
            elif 'Other' in x.text:         CURRENT_LIKES_TYPES.append('likes_other')
    except IndexError:
        raise ScrapingError("No likes for username %s" % graph_name)

    for likes_type in CURRENT_LIKES_TYPES:
        response = browser.get(LIKES_URL % (graph_name, likes_type))

        soup = BeautifulSoup(response.content.replace('<!--','').replace('-->',''))
        # print response.content

        for link in soup.findAll('a'):
            try:
                if link['title'] == link.text:

                    url = link['href']
                    name = link.text
                    result = (url, name)

                    try:
                        yield _result_to_model(result)
                    except ValueError:
                        continue

            except KeyError:
                continue

        cursor_tag = _find_script_tag(response.text, "enableContentLoader")
        cursor_data = _parse_cursor_data(cursor_tag) if cursor_tag else None

        if not cursor_data: continue
        
        ajax_data = {
            'collection_token': cursor_data[0][0],
            'cursor': cursor_data[0][1],
            'profile_id': cursor_data[0][0].split(':')[0],
            'tab_key': likes_type,
            'overview': 'false',
            'sk': 'likes',
            'ftid': 'null',
            'order': 'null',
            'importer_state': 'null'
        }

        while True:

            # print ajax_data

            payload = _get_payload(ajax_data, current_user.id)
            response = browser.get(AJAX_URL + "?%s" % urllib.urlencode(payload))
        
            # PARSE PAGE

            data = json.loads(response.content[9:])
            soup = BeautifulSoup(data['payload'])
            for link in soup.findAll('a'):
                try:
                    if link['title'] == link.text:
                        url = link['href']
                        name = link.text
                        result = (url, name)

                        try:
                            yield _result_to_model(result)
                        except ValueError:
                            continue

                except KeyError:
                    continue

            # FIND NEXT CURSOR

            regex = re.compile("href=\\\\\"(.*?)\"")

            tester = lambda x: x.find('cursor') != -1
            thing = regex.findall(response.text)
            thing2 = filter(tester, thing)

            # NO NEXT CURSOR FOUND

            if not thing2: break

            regex2 = re.compile("next_cursor=(.*)")
            new_cursor = regex2.findall(thing2[0])[0].replace("\\u00253D\\", "=").replace("u00253D\\", "=")

            ajax_data['cursor'] = new_cursor



