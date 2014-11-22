socialscraper
=========

pip install -e git://github.com/alpaca/socialscraper.git#egg=socialscraper --upgrade

Facebook Tests
```
python -m socialscraper.tests.integration.facebook
```

```
# see methods on the FacebookScraper class here:
# https://github.com/alpaca/socialscraper/blob/master/socialscraper/facebook/scraper.py
# such as get_about, get_feed, get_likes, get_fans

# or use the scraper's authenticated browser to scrape your own content
# scraper.browser.get("xxxx")
```
