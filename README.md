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

# How to Change Primary Key from uid to username

0.
```
dropdb buildchicago && createdb buildchicago
cat latest.dump.txt | psql buildchicago
```
1. Change FacebookFriend class to contain username1 and username2 columns.
```
username1 = Column("username1", "String")
username2 = Column("username2", "String")
```
2. Add username1 and username2 columns to facebook_friends.
```
ALTER TABLE facebook_friends ADD COLUMN username1 varchar;
ALTER TABLE facebook_friends ADD COLUMN username2 varchar;
```
3. Fill username1 and username2 for each row in the table.
```
python -i models.py

for item in session.query(FacebookFriend).all():
	item.username1 = session.query(FacebookUser).filter(FacebookUser.uid==item.uid1).first().username
	item.username2 = session.query(FacebookUser).filter(FacebookUser.uid==item.uid2).first().username
session.commit()
```
4. Change FacebookFriend class to remove uid1 and uid2 columns. Change username1 and username2 columns to be primary key.
5.
```
ALTER TABLE facebook_friends DROP CONSTRAINT facebook_friends_pkey;
ALTER TABLE facebook_friends DROP COLUMN uid1;
ALTER TABLE facebook_friends DROP COLUMN uid2;
ALTER TABLE facebook_friends ALTER COLUMN username1 SET NOT NULL;
ALTER TABLE facebook_friends ALTER COLUMN username2 SET NOT NULL;
ALTER TABLE facebook_friends ADD CONSTRAINT facebook_friends_pkey PRIMARY KEY (username1, username2);
ALTER TABLE facebook_friends DROP CONSTRAINT facebook_friends_uid1_fkey;
ALTER TABLE facebook_friends DROP CONSTRAINT facebook_friends_uid2_fkey;
ALTER TABLE facebook_friends ADD CONSTRAINT facebook_friends_username1_fkey FOREIGN KEY (username1) REFERENCES facebook_users (username) MATCH FULL;
ALTER TABLE facebook_friends ADD CONSTRAINT facebook_friends_username2_fkey FOREIGN KEY (username2) REFERENCES facebook_users (username) MATCH FULL;
```
6. Change FacebookUser class to have username as primary key.
7.
```
ALTER TABLE facebook_users DROP CONSTRAINT facebook_users_pkey CASCADE;
ALTER TABLE facebook_users ADD CONSTRAINT facebook_users_pkey PRIMARY KEY (username);
```
8. Change FacebookPagesUsers class to have username as a column.
9.
```
ALTER TABLE facebook_pages_users ADD COLUMN username;
```
10.
```
python -i models.py
for item in session.query(FacebookPagesUsers).all():
	item.username = session.query(FacebookUser).filter(FacebookUser.uid==item.uid).first().username
session.commit()
```
9. Change FacebookPagesUsers class to remove uid column. Change username column to be part of composite primary key.
10.
```
ALTER TABLE facebook_pages_users ALTER COLUMN username SET NOT NULL;
ALTER TABLE facebook_pages_users DROP CONSTRAINT facebook_pages_users_pkey CASCADE;
ALTER TABLE facebook_pages_users DROP COLUMN uid;
```

not sure?
```
ALTER TABLE facebook_pages_users DROP CONSTRAINT facebook_pages_users_page_id_fkey CASCADE;
```