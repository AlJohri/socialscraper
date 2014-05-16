import logging
from time import time
from datetime import datetime
from urlparse import urlparse, parse_qs
from facebook import GraphAPIError

from . import get_object

logger = logging.getLogger(__name__)

def get_feed(api, username, earlier_date=None, later_date=None):
    """

    get_feed grabs posts reverse chronologically. it "starts" at the date 
    specified in "until" and goes back in time until "since".

    if until is not specified, until is set to the current date

    if since is not specified, it grabs posts indefinitely in the past

    """
    
    if not later_date:
        until = int(time())
    else:
        until = later_date.strftime("%s")

    if not earlier_date:
        since = ""
    else:
        since = earlier_date.strftime("%s")


    def get_previous(previous_url):
        previous_url_parameters = parse_qs(urlparse(previous_url).query)
        return int(previous_url_parameters['since'][0])

    def get_next(next_url):
        next_url_parameters = parse_qs(urlparse(next_url).query)
        return int(next_url_parameters['until'][0])

    profile = get_object(api, username)

    while True:

        # print "Getting Feed Until: " + datetime.utcfromtimestamp(until).strftime('%Y-%m-%d %H:%M:%S')
        profile = api.get_object(username + "/feed", until=str(until), since=str(since))
        if profile['data'] == []:
            # print "End of Results"
            break
        # since = get_previous(profile['paging']['previous'])
        until = get_next(profile['paging']['next'])

        for item in profile['data']:
            yield item