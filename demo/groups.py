import os, sys; sys.path.append(os.path.abspath('../'))
import json

from facebook import GraphAPI, GraphAPIError
from socialscraper.facebook import graphapi
FACEBOOK_USER_TOKEN = os.getenv('FACEBOOK_USER_TOKEN')
api = GraphAPI(FACEBOOK_USER_TOKEN)


for group in graphapi.get_object(api, "357518484295082/groups")['data']:
	members = graphapi.get_object(api, group['id']+'/members')
	name = group['name']
