socialscraper
=========

pip install -e git://github.com/alpaca/socialscraper.git#egg=socialscraper --upgrade

```
import os, pickle, json, lxml.html
from socialscraper.facebook import FacebookScraper

scraper_type="nograph"

# ALWAYS cache the facebook_scraper to prevent logging in multiple times
if not os.path.isfile('facebook_scraper.pickle'):
   scraper = FacebookScraper(scraper_type=scraper_type)
   scraper.add_user(email=os.getenv('FACEBOOK_EMAIL'), password=os.getenv('FACEBOOK_EMAIL'))
   scraper.login()
else:
   scraper = pickle.load(open('facebook_scraper.pickle'))
   scraper.scraper_type = scraper_type

# see methods on the FacebookScraper class here:
# https://github.com/alpaca/socialscraper/blob/master/socialscraper/facebook/scraper.py
# such as get_about, get_feed, get_likes, get_fans

# or use the scraper's authenticated browser to scrape your own content
# scraper.browser.get("xxxx")
```
