import os, sys; sys.path.append(os.path.abspath('../'))
import json

from facebook import GraphAPI, GraphAPIError
from socialscraper.facebook import graphapi

from models import Session, FacebookUser, FacebookGroup
from lib import save_user, save_group

session = Session()

FACEBOOK_USER_TOKEN = os.getenv('FACEBOOK_USER_TOKEN')
api = GraphAPI(FACEBOOK_USER_TOKEN)
NORTHWESTERN_GROUP = "357518484295082"

for group in graphapi.get_groups(api, NORTHWESTERN_GROUP):
	print group
	save_group(group, session)
	for member in graphapi.get_members(api, group.uid):
		print member
		save_user(member, session)