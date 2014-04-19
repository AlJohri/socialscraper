import logging, requests, lxml.html, json, urllib, re
from ..base import ScrapingError

import pdb

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BASE_URL = 'https://www.facebook.com/%s'
AJAX_URL = "https://www.facebook.com/ajax/pagelet/generic.php/ProfileTimelineSectionPagelet"


from . import graph


import pprint
pp = pprint.PrettyPrinter(indent=4)


def search(browser, current_user, graph_name):

    graph_id = graph.get_id(graph_name)

    def _find_script_tag(raw_html, phrase):
        doc = lxml.html.fromstring(raw_html)
        script_tag = filter(lambda x: x.text_content().find(phrase) != -1, doc.cssselect('script'))
        if not script_tag: raise ScrapingError("Couldn't find script tag")
        return json.loads(script_tag[0].text_content()[24:-1])

    def _get_payload(ajax_data, uid, ajaxpipe_token, page):
        return {
            "ajaxpipe": 1,
            "ajaxpipe_token": ajaxpipe_token,
            "no_script_path": 1,
            "data": json.dumps(ajax_data),
            "__user": current_user.id,
            "__a": 1,
            "__dyn": "7n8ajEAMCBynzpQ9UoHaEWy6zECiq78hAKGgyiGGeqheCu6popG",
            "__req": "jsonp_22",
            "__rev": "1213535",
            "__adt": page
        }

    response = browser.get(BASE_URL % graph_name)
    cursor_tag = _find_script_tag(response.text, "section_container_id")
    
    regex = re.compile("{\"ajaxpipe_token\":\"(.*)\",\"lhsh\":\"(.*)\"}")
    r = regex.search(response.text)
    
    ajax_data = json.loads(str(cursor_tag['jscc_map'])[105:-93])
    del ajax_data['section_container_id']
    del ajax_data['section_pagelet_id']
    del ajax_data['unit_container_id']
    del ajax_data['current_scrubber_key']
    del ajax_data['require_click']
    # del ajax_data['num_visible_units']
    del ajax_data['buffer']
    del ajax_data['adjust_buffer']
    del ajax_data['showing_esc']
    del ajax_data['remove_dupes']
    # del ajax_data['tipld']

    # del ajax_data['start']
    # del ajax_data['end']

    # del ajax_data['tipld']['sc']
    # del ajax_data['tipld']['vc']
    # del ajax_data['tipld']['rc']

    # get first page
    for i in range(1,10):
        ajax_data['page_index'] = i
        ajax_data['tipld']['sc'] = 5 * (i-1)
        payload = _get_payload(ajax_data, current_user.id, r.groups()[0], i)
        # pp.pprint(payload)
        response = browser.get(AJAX_URL + "?%s" % urllib.urlencode(payload))
        doc = lxml.html.fromstring(response.text)
        test = doc.cssselect('script')[2].text_content()
        regex = re.compile("if \(self != top\) {parent\.require\(\"JSONPTransport\"\)\.respond\(\d, ({.*}),\"jsmods\"", re.MULTILINE|re.DOTALL)
        blah = regex.findall(test)[0]
        blah = blah + "}}"
        yay = json.loads(blah)
        da_html = yay['payload']['content']['_segment_' + str(i) + '_0_left']
        if not da_html: break
        uh = lxml.html.fromstring(da_html)

        for el in uh.cssselect('div[role]'):
            print el.text_content()
            print ""

    # # get second page
    # # ajax_data['start']
    # # ajax_data['end']
    # ajax_data['page_index'] = 3
    # payload = _get_payload(ajax_data, current_user.id, r.groups()[0])
    # pp.pprint(payload)
    # response = browser.get(AJAX_URL + "?%s" % urllib.urlencode(payload))
    # print response.text.decode('unicode-escape')



    # pdb.set_trace()


# ?no_script_path=1
# &data= {
#   "profile_id":1006531897,
#   "start":1230796800,
#   "end":1262332799,
#   "query_type":8,
#   "page_index":1,
#   "section_container_id":"u_jsonp_21_1",
#   "section_pagelet_id":"pagelet_timeline_year_2009",
#   "unit_container_id":"u_jsonp_21_0",
#   "current_scrubber_key":"year_2009",
#   "buffer":500,
#   "require_click":false,
#   "showing_esc":false,
#   "adjust_buffer":true,
#   "tipld":{"sc":8,"rc":7,"rt":1250609387,"vc":11},
#   "num_visible_units":11,
#   "remove_dupes":true
# }
# &__user=100000862956701
# &__a=1
# &__dyn=7n8ajEAMCBynzpQ9UoHaEWy6zECiq78hAKGgyiGGeqheCu6popG
# &__req=jsonp_22
# &__rev=1210030
# &__adt=22
