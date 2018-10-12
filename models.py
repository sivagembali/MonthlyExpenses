from flask_sqlalchemy import SQLAlchemy

from Expenses import app

db = SQLAlchemy(app)
class registerNew(db.Model):
    user_id = db.Column(db.String(50),primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    mobile = db.Column(db.Integer)
    password = db.Column(db.String(50))


class expenses(db.Model):
    entry_no=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.String(50))
    date = db.Column(db.DATE)
    type = db.Column(db.String(50))
    amount = db.Column(db.Integer)

#db.create_all()
