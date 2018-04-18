import datetime
from server.models import db

class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    title = db.Column(db.String(30), primary_key=False, unique=False, nullable=False)
    body = db.Column(db.Text, primary_key=False, unique=False, nullable=False)

    tags = db.relationship('Tag', secondary='record_tag')
    collaborators = db.relationship('User', secondary='record_user')

class RecordUser(db.Model):
    __tablename__ = 'record_user'

    record_id = db.Column(db.Integer,
        db.ForeignKey('records.id'),
        primary_key=True
    )

    user_id = db.Column(db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    )

    user = db.relationship(
        'User',
        cascade="save-update, merge, delete"
    )

    record = db.relationship(
        'Record',
        cascade="save-update, merge, delete"
    )
