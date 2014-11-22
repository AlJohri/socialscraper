import os, sys; sys.path.append(os.path.abspath('../'))
import csv

import pickle, logging, datetime
from socialscraper.facebook import FacebookScraper
# from socialscraper.adapters.adapter_sqlalchemy import convert_result

from models import Session, FacebookUser
from lib import save_user

# logging.basicConfig(level=logging.DEBUG)

session = Session()
scraper_type = "nograph"

if not os.path.isfile('facebook_scraper.pickle'):
    scraper = FacebookScraper(scraper_type=scraper_type)
    scraper.add_user(email=os.getenv('FACEBOOK_EMAIL'), password=os.getenv('FACEBOOK_PASSWORD'))
    scraper.login()
    scraper.init_api()
    pickle.dump(scraper, open('facebook_scraper.pickle', 'wb'))
else:
    scraper = pickle.load(open('facebook_scraper.pickle', 'rb'))
    scraper.scraper_type = scraper_type

# for i, result in enumerate(scraper.graph_search(None, "groups", 357518484295082))
# Example: Get groups of Facebook Group - 357518484295082 (Northwestern)
# data = [result[3] for i, result in enumerate(scraper.graph_search(None, "groups", 357518484295082))]
with open('groups.csv', 'wd') as f:
    writer = csv.writer(f)
    for i, result in enumerate(scraper.graph_search(None, "groups", 357518484295082)):
    	if i>387:
			writer.writerow([result[0], result[1], result[2].encode('utf-8'), result[3], result[4]])
			print('success')
		print i
