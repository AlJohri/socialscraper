import os, sys; sys.path.append(os.path.abspath('../'))

import pickle, logging, datetime, pickle
from models import Session, FacebookUser, FacebookGroup
from sqlalchemy import func
from lib import get_scraper, save_user

logging.basicConfig(level=logging.DEBUG)
session = Session()
scraper = get_scraper()

# # Example: Get members of Facebook Group - 357518484295082 (Northwestern)
# for i, result in enumerate(scraper.graph_search(None, "members", 357518484295082)):
#     save_user(result, session)

# # Example: Get friends of FacebookUser
# for i, result in enumerate(scraper.get_friends_nograph("andybayer")):
#     save_user(result, session)

# Change all FacebookGroup with 0 members to have privacy "not started". #HACK
# for group_id in session.query(FacebookGroup.group_id).outerjoin(FacebookGroup.users).group_by(FacebookGroup.group_id).having(func.count(FacebookUser.uid) == 0):
# 	group = session.query(FacebookGroup).filter(FacebookGroup.group_id == group_id[0]).first()
# 	group.privacy = "not started"
# 	session.commit()

# # Example: Get members of closed Facebook Groups
# for group_id in session.query(FacebookGroup.group_id).outerjoin(FacebookGroup.users).group_by(FacebookGroup.group_id).having(func.count(FacebookUser.uid) == 0):
# 	group = session.query(FacebookGroup).filter(FacebookGroup.group_id == group_id[0]).first()
# 	print group.group_id, group.name
	
# 	for member in scraper.get_members_nograph(group.group_id, group.group_id):
# 		print member.uid, member.name
# 		user = save_user(member, session)
# 		group.users.append(user)

# 	session.commit()