import os, sys; sys.path.append(os.path.abspath('../'))
from models import Session, FacebookUser, FacebookGroup
from socialscraper.adapters.adapter_sqlalchemy import convert_result

import datetime

def save_user(result, session):
    user = session.query(FacebookUser).filter_by(uid=result.uid).first()
    if not user:
        user = FacebookUser()
        convert_result(user, result)
        user.created_at = datetime.datetime.now()
        session.add(user)
        print user.name, "created"

    session.commit()

    return user

def save_group(result, session):
    group = session.query(FacebookGroup).filter_by(uid=result.uid).first()
    if not group:
        group = FacebookGroup()
        convert_result(group, result)
        group.created_at = datetime.datetime.now()
        session.add(group)
        print group.name, "created"