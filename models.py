from flask_sqlalchemy import SQLAlchemy

from Expenses import app

db = SQLAlchemy(app)
class registerNew(db.Model):
    name = db.Column(db.String(50))
    email = db.Column('email', db.String, primary_key = True)
    mobile = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    password = db.Column(db.String(50))






#db.create_all()