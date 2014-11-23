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


dontdoshit = True

for group in graphapi.get_groups(api, NORTHWESTERN_GROUP):
	if int(group.group_id) == 357858834261047: dontdoshit = False
	if dontdoshit == True: continue
	print group
	group = save_group(group, session)

	for member in graphapi.get_members(api, group.group_id):
		print member
		user = save_user(member, session)
		group.users.append(user)

	session.commit()