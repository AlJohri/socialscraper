import os, sys; sys.path.append(os.path.abspath('../'))

from facebook import GraphAPI, GraphAPIError
from socialscraper.facebook import graphapi
FACEBOOK_USER_TOKEN = os.getenv('FACEBOOK_USER_TOKEN')
api = GraphAPI(FACEBOOK_USER_TOKEN)

print graphapi.get_object(api, "al.johri")