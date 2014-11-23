from ..base import BaseModel, Column

class FacebookUser(BaseModel):
    __tablename__ = "facebook_users"
    __attrs__ = [
        'uid', 'username', 'email', 'birthday', 
        'name', 'locale', 'profile_url', 'sex',
        'college', 'employer', 'highschool', 'currentcity', 
        'hometown', 'misc', 'data', 'donor', 'contact_time',
        'scrape_status', 'nu'
    ]

    uid = Column("uid", "BigInteger", primary_key=True)
    username = Column("username")
    email = Column("email")
    birthday = Column("birthday", "Date")
    name = Column("name")
    locale = Column("locale")
    profile_url = Column("profile_url")
    sex = Column("sex")
    
    college = Column("college")
    employer = Column("employer")
    highschool = Column("highschool")
    currentcity = Column("currentcity")
    hometown = Column("hometown")
    misc = Column("misc")
    data = Column("data")
    donor = Column("donor", "String")
    contact_time = Column("contact_time")
    scrape_status = Column("scrape_status", "Integer") # empty = not attempted, 0 = can't get likes, 1 = scrape in progress, 2 = scrape finished
    nu = Column("nu", "Integer")

class FacebookFamily(BaseModel):
    __tablename__ = "facebook_families"
    __attrs__ = ['profile_id', 'relationship', 'uid', 'name']

    profile_id = Column("profile_id", "BigInteger", primary_key=True, foreign_key=True, foreign_key_reference="facebook_users.uid")
    relationship = Column("relationship")
    uid = Column("uid","BigInteger", primary_key=True, foreign_key=True, foreign_key_reference="facebook_users.uid") # foreign key
    name = Column("name")

class FacebookPage(BaseModel):
    __tablename__ = "facebook_pages"
    __attrs__ = [
        'about', 'username', 'page_id', 'is_verified', 
        'keywords', 'name', 'url', 'type', 'num_likes',
        'talking_about_count', 'hometown', 'misc', 'data'
    ]

    about = Column("about","Text")
    username = Column("username")
    page_id = Column("page_id","BigInteger", primary_key=True) # primary key
    is_verified = Column("is_verified","Boolean")
    keywords = Column("keywords")
    # location = Column("location","BigInteger", foreign_key=True, foreign_key_reference="facebook_locations.loc_id") # foreign key
    name = Column("name")
    url = Column("url")
    type = Column("type")
    num_likes = Column("num_likes","BigInteger")
    talking_about_count = Column("talking_about_count", "BigInteger")
    hometown = Column("hometown")
    misc = Column("misc")
    data = Column("data")

class FacebookStatus(BaseModel):
    __tablename__ = "facebook_statuses"    
    __attrs__ = ['like_count', 'message', 'status_id', 'uid', 'time']

    like_count = Column("like_count","Integer")
    message = Column("message","Text")
    status_id = Column("status_id","BigInteger", primary_key=True)
    uid = Column("uid","BigInteger")
    time = Column("time","Date")

class FacebookLocation(BaseModel):
    __tablename__ = "facebook_locations"
    __attrs__ = [
        'gid', 'loc_id', 'street', 'city', 
        'state', 'country', 'zip', 'address', 
        'latitude', 'longitude', 'name'
    ]

    gid = Column("gid", "BigInteger")
    loc_id = Column("loc_id", "BigInteger", primary_key=True)
    street = Column("street")
    city = Column("city")
    state = Column("state")
    country = Column("country")
    zip = Column("zip")
    address = Column("address")
    latitude = Column("latitude")
    longitude = Column("longitude")
    name = Column("name")

class FacebookGroup(BaseModel):
    __tablename__ = "facebook_groups"
    __attrs__ = ['group_id', 'username', 'url', 'name']

    group_id = Column("group_id", "BigInteger", primary_key=True)
    username = Column("username")
    url = Column("url")
    name = Column("name")
    size = Column("size", "Integer")
    description = Column("description")
    icon = Column("icon")
    privacy = Column("privacy")


    #ALTER TABLE facebook_groups ADD COLUMN size integer;
    #ALTER TABLE facebook_groups ADD COLUMN description text;
    #ALTER TABLE facebook_groups ADD COLUMN icon text;
    #ALTER TABLE facebook_groups ADD COLUMN privacy text; 



######################################## Join Tables ########################################

class FacebookFriend(BaseModel):
    __tablename__ = "facebook_friends"
    __attrs__ = ['uid1', 'uid2']

    uid1 = Column("uid1", "BigInteger", primary_key=True, unique=False, foreign_key=True, foreign_key_reference="facebook_users.uid")
    uid2 = Column("uid2", "BigInteger", primary_key=True, unique=False, foreign_key=True, foreign_key_reference="facebook_users.uid")


class FacebookPagesUsers(BaseModel):
    __tablename__ = "facebook_pages_users"
    __attrs__ = ['uid', 'page_id', 'type']

    uid = Column("uid", "BigInteger", primary_key=True, unique=False, foreign_key=True, foreign_key_reference="facebook_users.uid")
    page_id = Column("page_id", "BigInteger", primary_key=True, unique=False, foreign_key=True, foreign_key_reference="facebook_pages.page_id")
    type = Column("type")

class FacebookGroupsUsers(BaseModel):
    __tablename__ = "facebook_groups_users"
    __attrs__ = ['uid', 'group_id']

    uid = Column("uid", "BigInteger", primary_key=True, unique=False, foreign_key=True, foreign_key_reference="facebook_users.uid")
    group_id = Column("group_id", "BigInteger", primary_key=True, unique=False, foreign_key=True, foreign_key_reference="facebook_groups.group_id")

__all__ = [
    'FacebookUser',
    'FacebookFamily',
    'FacebookPage',
    'FacebookStatus',
    'FacebookLocation',
    'FacebookFriend',
    'FacebookPagesUsers',
    'FacebookGroup'
]

