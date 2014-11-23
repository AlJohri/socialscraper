import os, sys; sys.path.append(os.path.abspath('../'))

import pickle, logging, datetime, pickle, requests, csv
from models import Session, FacebookUser, FacebookGroup, SuperGroup
from sqlalchemy import func
from lib import get_scraper, save_user
from pprint import pprint as pp

logging.basicConfig(level=logging.DEBUG)
session = Session()

def get_groups(dl=False):
    if not os.path.isfile("groups.csv") or os.path.getsize("groups.csv") == 0 or dl:
        print "Downloading groups.csv.."
        response = requests.get("https://docs.google.com/spreadsheets/d/1XHKzrw1XhAE0uumGyFdwgyN3HzQDRZvfFLCuY2EUTwA/export?format=csv")
        with open("groups.csv", "w") as f: f.write(response.content)
        print "Download complete."

    with open("groups.csv", "r") as f:
	    reader = csv.reader(f)
	    next(reader) # skip header
	    groups = filter(lambda x: x != None, [row if row[4] != "Trash" else None for row in reader])

    return groups

groups = get_groups()

for group_id, name, num_members, new_name, category, _ in groups:
	
	group = session.query(FacebookGroup).filter(FacebookGroup.group_id == int(group_id)).first()
	
	super_group_parent = session.query(SuperGroup).filter(SuperGroup.name == category).first()
	if not super_group_parent:
		super_group_parent = SuperGroup(name=category)
		session.add(super_group_parent)

	super_group = session.query(SuperGroup).filter(SuperGroup.name == new_name).first()
	if not super_group:
		super_group = SuperGroup(name=new_name)
		session.add(super_group)

	if super_group not in super_group_parent.children:
		super_group_parent.children.append(super_group)

	group.supergroup_id = super_group.id
	session.commit()

	print "Group:", group.group_id, group.name
	print "Category:", super_group_parent.id, super_group_parent.name
	print "Normalized Group:", super_group.id, super_group.name
