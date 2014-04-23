from ..base import BaseModel, Column

__all__ = ['FacebookUser', 'FacebookFamily', 'FacebookLocation', 'FacebookFriend', 'FacebookPage', 'FacebookCategoriesPages', 'FacebookStatus', 'FacebookPagesUsers']

class FacebookUser(BaseModel):
    __tablename__ = "facebook_users"

    uid = Column("uid", "BigInteger", primary_key=True)
    username = Column("username")
    email = Column("email")
    birthday = Column("birthday", "Date")
    name = Column("name")
    locale = Column("locale")
    profile_url = Column("profile_url")
    sex = Column("sex")

class FacebookFamily(BaseModel):
    __tablename__ = "facebook_families"

    profile_id = Column("profile_id", "BigInteger", primary_key=True, foreign_key=True, foreign_key_reference="facebook_users.uid")
    relationship = Column("relationship","String")
    uid = Column("uid","BigInteger", primary_key=True, foreign_key=True, foreign_key_reference="facebook_users.uid") # foreign key
    name = Column("name","String")

class FacebookFriend(BaseModel):
    __tablename__ = "facebook_friends"

    uid1 = Column("uid1","BigInteger",primary_key=True, foreign_key=True, foreign_key_reference="facebook_users.uid")
    uid2 = Column("uid2","BigInteger",primary_key=True, foreign_key=True, foreign_key_reference="facebook_users.uid")

class FacebookPage(BaseModel):
    __tablename__ = "facebook_pages"

    about = Column("about","Text")
    username = Column("username","String")
    page_id = Column("page_id","BigInteger", primary_key=True) # primary key
    is_verified = Column("is_verified","Boolean")
    keywords = Column("keywords","String")
    # location = Column("location","BigInteger", foreign_key=True, foreign_key_reference="facebook_locations.loc_id") # foreign key
    name = Column("name","String")
    url = Column("url","String")
    type = Column("type","String")
    num_likes = Column("num_likes","BigInteger")

class FacebookStatus(BaseModel):
    __tablename__ = "facebook_statuses"

    like_count = Column("like_count","Integer")
    message = Column("message","Text")
    status_id = Column("status_id","BigInteger", primary_key=True)
    uid = Column("uid","BigInteger")
    time = Column("time","Date")

class FacebookLocation(BaseModel):
    __tablename__ = "facebook_locations"

    gid = Column("gid", "BigInteger")
    loc_id = Column("loc_id", "BigInteger", primary_key=True)
    street = Column("street", "String")
    city = Column("city", "String")
    state = Column("state", "String")
    country = Column("country", "String")
    zip = Column("zip", "String")
    address = Column("address", "String")
    latitude = Column("latitude", "Float")
    longitude = Column("longitude", "Float")
    name = Column("name", "String")

# class FacebookCategory(BaseModel):
#     __tablename__ = "facebook_categories"

######################################## Join Tables ########################################

class FacebookCategory(BaseModel):
    __tablename__ = "facebook_categories"

class FacebookPagesUsers(BaseModel):
    __tablename__ = "facebook_pages_users"

    uid = Column("uid","BigInteger",primary_key=True, foreign_key=True, foreign_key_reference="facebook_users.uid")
    page_id = Column("page_id","BigInteger",primary_key=True, foreign_key=True, foreign_key_reference="facebook_pages.page_id")
    type = Column("type","String")
    created_time = Column("created_time","Date")

class FacebookCategoriesPages(BaseModel):
    __tablename__ = "facebook_categories_pages"

    page_id = Column("page_id","BigInteger",primary_key=True)
    category = Column("category","String",primary_key=True)

