import datetime
from server.models import db

class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    title = db.Column(db.String(30), primary_key=False, unique=False, nullable=False)
    body = db.Column(db.Text, primary_key=False, unique=False, nullable=False)

    tags = db.relationship('Tag')
    collaborators = db.relationship('User')
    posts = db.relationship('Post')
