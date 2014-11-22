import os, pickle, logging
from socialscraper.facebook import FacebookScraper

logging.basicConfig(level=logging.DEBUG)

scraper_type = "nograph"

if not os.path.isfile('facebook_scraper.pickle'):
   scraper = FacebookScraper(scraper_type=scraper_type)
   scraper.add_user(email=os.getenv('FACEBOOK_EMAIL'), password=os.getenv('FACEBOOK_PASSWORD'))
   scraper.login()
   pickle.dump(scraper, open('facebook_scraper.pickle', 'wb'))
else:
   scraper = pickle.load(open('facebook_scraper.pickle', 'rb'))
   scraper.scraper_type = scraper_type

for i,item in enumerate(scraper.get_friends_nograph("andybayer")):
    print item