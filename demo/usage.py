import os, sys; sys.path.append(os.path.abspath('../'))

import pickle, logging, datetime, pickle
from models import Session, FacebookUser, FacebookGroup
from sqlalchemy import func
from lib import get_scraper, save_user

logging.basicConfig(level=logging.DEBUG)
session = Session()
scraper = get_scraper()

# # Example: Get members of Facebook Group - 357518484295082 (Northwestern) using Graph Search Scraper
# for i, result in enumerate(scraper.graph_search(None, "members", 357518484295082)):
#     save_user(result, session)

# # Example: Get members of Facebook Group - 357518484295082 (Northwestern) using API
# FACEBOOK_USER_TOKEN = os.getenv('FACEBOOK_USER_TOKEN')
# api = GraphAPI(FACEBOOK_USER_TOKEN)
# NORTHWESTERN_GROUP = "357518484295082"
# for i, result in enumerate(graphapi.get_groups(api, NORTHWESTERN_GROUP)):
# 	print result
# 	group = save_group(result, session)
# 	group.privacy = result.privacy
# 	group.icon = result.icon
# 	session.commit()

# # Example: Get friends of FacebookUser
# for i, result in enumerate(scraper.get_friends_nograph("andybayer")):
#     save_user(result, session)

# # Example: Groups that have 0 members
# for group_id in session.query(FacebookGroup.group_id).outerjoin(FacebookGroup.users).group_by(FacebookGroup.group_id).having(func.count(FacebookUser.uid) == 0):
# 	group = session.query(FacebookGroup).filter(FacebookGroup.group_id == group_id[0]).first()
# 	print group.group_id, group.name

# for group in session.query(FacebookGroup).filter(FacebookGroup.privacy == "CLOSED").all():
# 	group.status = "todo"
# 	session.commit()

# Example: Get members of closed Facebook Groups
for group in session.query(FacebookGroup).filter(FacebookGroup.status == "in progress").all():
	
	for member in scraper.get_members_nograph(group.group_id, group.group_id):
		print member.uid, member.name
		user = save_user(member, session)
		group.users.append(user)

	group.status = "done"
	
	session.commit()

for group in session.query(FacebookGroup).filter(FacebookGroup.status == "todo").all():

	group.status = "in progress"
	session.commit()
	
	for member in scraper.get_members_nograph(group.group_id, group.group_id):
		print member.uid, member.name
		user = save_user(member, session)
		group.users.append(user)
	
	group.status = "done"
	session.commit()
