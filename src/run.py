# RUN ON PRODUCTION

from src.app import app as application, api, UserList  # for example, should be app
from src.db import db
from src.urls import *

db.init_app(application)


# it works automatic before first request
@application.before_first_request
def create_tables():
    db.create_all()
