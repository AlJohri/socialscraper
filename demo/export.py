import os, sys; sys.path.append(os.path.abspath('../'))

import csv
from models import Session, FacebookUser

session = Session()

with open("users.csv", "w") as f:
	writer = csv.writer(f)
	for user in session.query(FacebookUser).all():
		writer.writerow([user.uid, user.username, user.name.encode('utf-8')])