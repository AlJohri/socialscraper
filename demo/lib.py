import os, sys; sys.path.append(os.path.abspath('../'))
from models import Session, FacebookUser
from socialscraper.adapters.adapter_sqlalchemy import convert_result

def save_user(result, session):
    user = session.query(FacebookUser).filter_by(uid=result.uid).first()
    if not user:
        user = FacebookUser()
        convert_result(user, result)
        user.created_at = datetime.datetime.now()
        session.add(user)
        print user.name, "created"
    else:
        convert_result(user, result)
        print user.name, "updated"
    user.updated_at = datetime.datetime.now()
    session.commit()