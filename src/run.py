from app import app
from db import db

db.init_app(app)


# just like the line ==>  with app.app_context()  ==> no need to call function manual.
# it works automatic before first request
@app.before_first_request
def create_tables():
    db.create_all()