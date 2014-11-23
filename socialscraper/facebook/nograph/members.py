# -*- coding: utf-8 -*-

import re, json, lxml, urllib
from bs4 import BeautifulSoup
from ...base import ScrapingError
from ..models import FacebookUser

from ..import graphapi, public


def get_members(browser, current_user, graph_name, graph_id = None, api = None):


    def _result_to_model(result):

        url = result[0]
        name = result[1]

        username = public.parse_url(url)

        if api:
            uid, category = graphapi.get_attributes(api, username, ["id", "category"])
        else:
            uid, category = public.get_attributes(username, ["id", "category"])

        if uid == None: 
            print "Couldn't find UID of %s"
            raise ValueError("Couldn't find uid of %s" % username)

        uid = int(uid) if uid else None

        return FacebookUser(uid=uid, username=username, url=url, name=name)


    response = browser.get("https://www.facebook.com/groups/%s/" % graph_id)
    soup = BeautifulSoup(response.content.replace('<!--','').replace('-->',''))
    num_members_text = soup.find(text=re.compile("Members\s\(\d+\)"))
    if num_members_text: num_members = int(num_members_text.replace("Members (", "").replace(")", ""))

    step = 97
    for page in range(1,num_members,step):
        
        response = browser.get("https://www.facebook.com/ajax/browser/list/group_members/?id=%s&gid=%s&edge=groups%%3Amembers&order=default&view=list&start=%d&__a=1" % (graph_id, graph_id, page))
        data = json.loads(response.content[9:])
        
        try:
            doc = lxml.html.fromstring(data['domops'][0][3]['__html'])
        except lxml.etree.XMLSyntaxError as e:
            continue
        
        current_results = filter(lambda (url,name): name != '' and name != 'See More' and name != 'FriendFriends', map(lambda x: (x.get('href'), unicode(x.text_content())) , doc.cssselect('a')))
        
        for result in current_results:  yield _result_to_model(result)