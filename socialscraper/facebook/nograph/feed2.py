import logging, lxml.html, json, urllib, re, datetime, dateutil, collections, urlparse
# from .models import FacebookUser, FacebookStatus

from .. import public

logger = logging.getLogger(__name__)

BASE_URL = 'https://www.facebook.com/%s'
AJAX_URL = "https://www.facebook.com/ajax/pagelet/generic.php/PagePostsSectionPagelet"
regex_4real = re.compile("if \(self != top\) {parent\.require\(\"JSONPTransport\"\)\.respond\(\d+, ({.*}),\"jsmods\"", re.MULTILINE|re.DOTALL)

from enum import Enum
class QueryType(Enum):
    everything = 25
    highlights = 8
    recent = 36

import pprint
pp = pprint.PrettyPrinter(indent=4)

def get_feed2(browser, current_user, graph_name, graph_id = None, api = None):

    if not graph_id:
        graph_id = public.get_id(graph_name)

    def _find_script_tag(raw_html, phrase, index):
        doc = lxml.html.fromstring(raw_html)
        script_tag = filter(lambda x: x.text_content().find(phrase) != -1, doc.cssselect('script'))
        if not script_tag: return None
        return json.loads(script_tag[index].text_content()[24:-1])

    def _get_payload(ajax_data, uid, ajaxpipe_token, page):
        payload = collections.OrderedDict()
        payload['data'] = json.dumps(ajax_data)
        payload['__user'] = current_user.id
        payload['__a'] = 1
        payload['__dyn'] = "7n8anEAMCBynzpQ9UoHFaeExEW9J6yUgByV9GiyGGEVFLO0xBxC9V8CdBUgDyQqVayahk"
        payload['__req'] = "1f"
        payload['__rev'] = 1377599
        # payload['ajaxpipe'] = 1
        # payload['ajaxpipe_token'] = ajaxpipe_token
        return payload

    response = browser.get(BASE_URL % graph_name)
    cursor_tag = _find_script_tag(response.text, "PagesPostsSection", 1)
    if not cursor_tag: raise "couldn't find PagesPostsSection"

    # ajax_data = cursor_tag['jsmods']['instances'][4][2][2]
    # del ajax_data['post_section']['filter_after_timestamp']

    regex = re.compile("{\"ajaxpipe_token\":\"(.*)\",\"lhsh\":\"(.*)\"}")
    r = regex.search(response.text)

    # datetime.datetime.fromtimestamp(1398927599)
    # datetime.datetime(2012,04,01,0,0).strftime('%s')
    tNow = datetime.datetime.now()
    start = datetime.date(tNow.year, tNow.month, 1)
    end = datetime.date(tNow.year, tNow.month+1, 1)

    while True:

        print start.strftime("%A %d %B %Y") + " to " + end.strftime("%A %d %B %Y")

        page_counter = 0

        while True:

            segment_counter = 0

            while True:

                ajax_data = collections.OrderedDict()
                ajax_data['segment_index'] = segment_counter
                ajax_data['page_index'] = page_counter
                ajax_data['page'] = graph_id
                ajax_data['column'] = "main"
                ajax_data['post_section'] = collections.OrderedDict()
                ajax_data['post_section']['profile_id'] = graph_id
                ajax_data['post_section']['start'] = start.strftime('%s')
                ajax_data['post_section']['end'] = end.strftime('%s')
                ajax_data['post_section']['query_type'] = QueryType.everything.value
                ajax_data['post_section']['filter'] = 1
                ajax_data['post_section']['is_pages_redesign'] = True
                ajax_data['section_index'] = 0
                ajax_data['hidden'] = False
                # ajax_data['posts_loaded'] = posts_counter
                ajax_data['show_all_posts'] = True

                payload = _get_payload(ajax_data, current_user.id, r.groups()[0], page_counter)
                response = browser.get(AJAX_URL + "?%s" % urllib.urlencode(payload))

                data = json.loads(response.content[9:])
                if not data['payload']:
                    # print page_counter, segment_counter, "No Results"
                    break
                doc = lxml.html.fromstring(data['payload'])
                # pp.pprint(dict(ajax_data.items()))
                for article in doc.cssselect("div[role]"):

                    heading = article.cssselect('h5')[0].text_content().strip()
                    if not heading == "Killed By Police shared a link.": continue

                    text = article.cssselect('.userContent')[0].text_content()
                    relative_time_posted = article.cssselect('.uiLinkSubtle')[0].text_content()
                    fb_url = article.cssselect('.uiLinkSubtle')[0].get('href')
                    raw_url = article.cssselect('h5 a[onmouseover]')[0].get('href')
                    real_url = urlparse.parse_qs(urlparse.urlparse(raw_url).query)['u'][0]

                    print text + "\t" + fb_url + "\t" + real_url


                segment_counter += 1

            start += dateutil.relativedelta.relativedelta(months=-1)
            end += dateutil.relativedelta.relativedelta(months=-1)

            if end < datetime.date(2004,1,1):
                break
