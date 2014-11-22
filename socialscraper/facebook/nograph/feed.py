import logging, lxml.html, json, urllib, re, datetime, dateutil
# from .models import FacebookUser, FacebookStatus

from .. import public

logger = logging.getLogger(__name__)

BASE_URL = 'https://www.facebook.com/%s'
AJAX_URL = "https://www.facebook.com/ajax/pagelet/generic.php/ProfileTimelineSectionPagelet"
regex_4real = re.compile("if \(self != top\) {parent\.require\(\"JSONPTransport\"\)\.respond\(\d+, ({.*}),\"jsmods\"", re.MULTILINE|re.DOTALL)

from enum import Enum
class QueryType(Enum):
    everything = 25
    highlights = 8
    recent = 36

import pprint
pp = pprint.PrettyPrinter(indent=4)

def get_feed(browser, current_user, graph_name, graph_id = None, api = None):

    if not graph_id:
        graph_id = public.get_id(graph_name)

    def _find_script_tag(raw_html, phrase):
        doc = lxml.html.fromstring(raw_html)
        script_tag = filter(lambda x: x.text_content().find(phrase) != -1, doc.cssselect('script'))
        if not script_tag: return None
        return json.loads(script_tag[0].text_content()[24:-1])

    def _get_payload(ajax_data, uid, ajaxpipe_token, page):
        return {
            "ajaxpipe": 1,
            "ajaxpipe_token": ajaxpipe_token,
            "data": json.dumps(ajax_data),
            "__user": current_user.id,
            "__dyn": "7n8ajEAMCBynzpQ9UoHaEWy6zECiq78hAKGgyiGGeqheCu6popG",
        }

    response = browser.get(BASE_URL % graph_name)
    cursor_tag = _find_script_tag(response.text, "section_container_id")
    if not cursor_tag: return None
    
    regex = re.compile("{\"ajaxpipe_token\":\"(.*)\",\"lhsh\":\"(.*)\"}")
    r = regex.search(response.text)
    
    ajax_data = json.loads(str(cursor_tag['jscc_map'])[105:-93])

    del ajax_data['section_container_id']
    del ajax_data['section_pagelet_id']
    del ajax_data['unit_container_id']
    del ajax_data['current_scrubber_key']
    del ajax_data['require_click']
    del ajax_data['buffer']
    del ajax_data['adjust_buffer']
    del ajax_data['showing_esc']
    del ajax_data['remove_dupes']
    del ajax_data['num_visible_units']
    del ajax_data['tipld']

    ajax_data['query_type'] = QueryType.everything.value

    # datetime.datetime.fromtimestamp(1398927599)
    # datetime.datetime(2012,04,01,0,0).strftime('%s')
    tNow = datetime.datetime.now()
    start = datetime.date(tNow.year, tNow.month, 1)
    end = datetime.date(tNow.year, tNow.month+1, 1)

    while True:
        start += dateutil.relativedelta.relativedelta(months=-1)
        end += dateutil.relativedelta.relativedelta(months=-1)

        logger.info(start.strftime("%A %d %B %Y") + "to" + end.strftime("%A %d %B %Y"))

        ajax_data['start'] = start.strftime('%s') 
        ajax_data['end'] = end.strftime('%s')

        page_counter = 0

        while True:
            ajax_data['page_index'] = page_counter
            payload = _get_payload(ajax_data, current_user.id, r.groups()[0], page_counter)
            response = browser.get(AJAX_URL + "?%s" % urllib.urlencode(payload))
            doc = lxml.html.fromstring(response.text)
            
            test = doc.cssselect('script')[2].text_content()
            blah = regex_4real.findall(test)[0]
            blah = blah + "}}"
            yay = json.loads(blah)
            da_html = yay['payload']['content'].get('_segment_' + str(page_counter) + '_0_left', None)
            if not da_html: da_html = yay['payload']['content'].get('_segment_0_0', None)

            test2 = doc.cssselect('script')[4].text_content()
            if len(test2) > 750:
                blah2 = regex_4real.findall(test2)[0]
                blah2 = blah2 + "}}"
                yay2 = json.loads(blah2)
                da_html2 = yay2['payload']['content'].get('_segment_' + str(page_counter) + '_1_left', None)
                if not da_html2: da_html2 = yay2['payload']['content'].get('_segment_0_0', None)
            else:
                da_html2 = None
            
            if da_html: 
                uh = lxml.html.fromstring(da_html)
                for el in uh.cssselect('div[role]'):
                    print el.text_content()
                    print ""
            if da_html2:
                uh2 = lxml.html.fromstring(da_html2)
                for el2 in uh2.cssselect('div[role]'):
                    print el2.text_content()
                    print ""

            if not da_html and not da_html2:
                break

            page_counter += 1

        # if not da_html and page_counter == 0: 
        #     pp.pprint(payload)
        #     break

        if end < datetime.date(2004,1,1):
            break