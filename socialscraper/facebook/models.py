from ..base import BaseModel, Column

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
    
    college = Column("college")
    employer = Column("employer")
    highschool = Column("highschool")
    currentcity = Column("currentcity")
    hometown = Column("hometown")

class FacebookFamily(BaseModel):
    __tablename__ = "facebook_families"

    profile_id = Column("profile_id", "BigInteger", primary_key=True, foreign_key=True, foreign_key_reference="facebook_users.uid")
    relationship = Column("relationship")
    uid = Column("uid","BigInteger", primary_key=True, foreign_key=True, foreign_key_reference="facebook_users.uid") # foreign key
    name = Column("name")

class FacebookPage(BaseModel):
    __tablename__ = "facebook_pages"

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
    street = Column("street")
    city = Column("city")
    state = Column("state")
    country = Column("country")
    zip = Column("zip")
    address = Column("address")
    latitude = Column("latitude")
    longitude = Column("longitude")
    name = Column("name")

# class FacebookCategory(BaseModel):
#     __tablename__ = "facebook_categories"

######################################## Join Tables ########################################


class FacebookFriend(BaseModel):
    __tablename__ = "facebook_friends"

    uid1 = Column("uid1","BigInteger", primary_key=True, foreign_key=True, foreign_key_reference="facebook_users.uid")
    uid2 = Column("uid2","BigInteger", primary_key=True, foreign_key=True, foreign_key_reference="facebook_users.uid")

class FacebookPagesUsers(BaseModel):
    __tablename__ = "facebook_pages_users"

    uid = Column("uid","BigInteger", primary_key=True, foreign_key=True, foreign_key_reference="facebook_users.uid")
    page_id = Column("page_id","BigInteger", primary_key=True, foreign_key=True, foreign_key_reference="facebook_pages.page_id")
    type = Column("type")
    created_time = Column("created_time","Date")

# class FacebookCategoriesPages(BaseModel):
#     __tablename__ = "facebook_categories_pages"

#     page_id = Column("page_id","BigInteger",primary_key=True)
#     category = Column("category",primary_key=True)

__all__ = ['FacebookUser', 'FacebookFamily', 'FacebookLocation', 'FacebookFriend', 'FacebookPage', 'FacebookStatus', 'FacebookPagesUsers']