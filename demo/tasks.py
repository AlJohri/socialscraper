import os, sys; sys.path.append(os.path.abspath('../'))

from models import Session, FacebookUser
from celery import Celery

app = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')

@app.task
def add(x, y):
	# session = Session()
    return x + y

# celery -A tasks worker --loglevel=info