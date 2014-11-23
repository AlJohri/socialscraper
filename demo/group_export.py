import os, sys; sys.path.append(os.path.abspath('../'))
import json
import csv

from facebook import GraphAPI, GraphAPIError
from socialscraper.facebook import graphapi

from models import Session, FacebookUser, FacebookGroup
from lib import save_user, save_group

session = Session()

FACEBOOK_USER_TOKEN = os.getenv('FACEBOOK_USER_TOKEN')
api = GraphAPI(FACEBOOK_USER_TOKEN)
NORTHWESTERN_GROUP = "357518484295082"


		# writer.writerow([result[0], result[1], result[2].encode('utf-8'), result[3], result[4]])

with open('groups.csv', 'wd') as f:
    writer = csv.writer(f)
    for i, result in enumerate(graphapi.get_groups(api, NORTHWESTERN_GROUP)):
		writer.writerow([result.group_id, result.name.encode('utf-8')])