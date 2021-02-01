from app import app as application  # for example, should be app
from db import db

db.init_app(application)


# it works automatic before first request
@application.before_first_request
def create_tables():
    db.create_all()
