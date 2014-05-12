# -*- coding: utf-8 -*-

import re, json, lxml, urllib
from bs4 import BeautifulSoup
from ...base import ScrapingError

# TODO: write a nograph likes scraper

"""
notes:

likes_recent # didn't work?
likes_sports_teams # didn't work?
likes_activities # didn't work?
likes_interests # didn't work?
likes_athletes # didn't work?
likes_websites # didn't work?
likes_foods # didn't work?

https://www.facebook.com/al.johri/sports

https://www.facebook.com/ajax/pagelet/generic.php/ManualCurationOGGridCollectionPagelet?data={"collection_token":"529398993:2409997254:45","cursor":"MDpub3Rfc3RydWN0dXJlZDoyNzYwMTA0ODEyMDE=","tab_key":"likes_other","profile_id":529398993,"overview":false,"ftid":null,"order":null,"sk":"likes","importer_state":null}&__user=100000862956701&__a=1&__dyn=7n8ahyj2qmumdDgDxyIJ3Ga58Ciq2W8GA8ABGeqheCu6popGiGw&__req=n&__rev=1243607

http://graph.facebook.com/738743013
738743013:2409997254:45
collection_token <dudeyourscrapinid>:2409997254:45

data={
    "collection_token":"529398993:2409997254:45",
    "cursor":"MDpub3Rfc3RydWN0dXJlZDoyNzYwMTA0ODEyMDE=",
    "tab_key":"likes_other",
    "profile_id":529398993,
    "overview":false,
    "ftid":null,
    "order":null,
    "sk":"likes",
    "importer_state":null
}
__user=100000862956701
__a=1
__dyn=7n8ahyj2qmumdDgDxyIJ3Ga58Ciq2W8GA8ABGeqheCu6popGiGw
__req=n
__rev=1243607

MDpub3Rfc3RydWN0dXJlZDoxMTQ2MDEyNDE4ODgxMjc=
0:not_structured:114601241888127

MDpub3Rfc3RydWN0dXJlZDoyNzYwMTA0ODEyMDE=
0:not_structured:276010481201

MDpub3Rfc3RydWN0dXJlZDoxMTI0ODg0NDA0NTg=
0:not_structured:112488440458

"""

AJAX_URL = "https://www.facebook.com/ajax/pagelet/generic.php/ManualCurationOGGridCollectionPagelet"
LIKES_URL = "https://www.facebook.com/%s/%s"

# LIKES_TYPES = [
#   'likes_people', 
#   'likes_restaurants', 
#   'likes_sports', 
#   'likes_clothing', 
#   'likes_other'
# ]

LIKES_TYPES = ['likes_other']

def get_likes(browser, current_user, graph_name, graph_id = None):

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

    for likes_type in LIKES_TYPES:
        response = browser.get(LIKES_URL % (graph_name, likes_type))
        # parse 1st page here

        # parse response first page

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

        payload = _get_payload(ajax_data, current_user.id)

        print AJAX_URL + "?%s" % urllib.urlencode(payload)

        response = browser.get(AJAX_URL + "?%s" % urllib.urlencode(payload))

        # parse response (2nd page)
    
        data = json.loads(response.content[9:])
        soup = BeautifulSoup(data['payload'])
        for link in soup.findAll('a'):
            try:
                title = link['title']
                name = link.text
                href = link['href']

                yield {
                    "title": title,
                    "name": name,
                    "href": href
                }
            except KeyError:
                pass
        # import pdb; pdb.set_trace()


        regex = re.compile("href=\\\\\"(.*?)\"")

        tester = lambda x: x.find('cursor') != -1
        thing = regex.findall(response.text)
        thing2 = filter(tester, thing)

        if not thing2: continue

        regex2 = re.compile("next_cursor=(.*)")
        new_cursor = regex2.findall(thing2[0])[0].replace("\\u00253D\\", "=")

        ajax_data['cursor'] = new_cursor

        payload2 = _get_payload(ajax_data, current_user.id)
        response = browser.get(AJAX_URL + "?%s" % urllib.urlencode(payload2))

        print AJAX_URL + "?%s" % urllib.urlencode(payload2)
        return response

