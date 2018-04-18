import datetime
from server.models import db

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(30), primary_key=False, unique=True, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

class RecordTag(db.Model):
    __tablename__ = 'record_tag'

    record_id = db.Column(db.Integer,
        db.ForeignKey('records.id'),
        primary_key=True
    )

    tag_id = db.Column(db.Integer,
        db.ForeignKey('tags.id'),
        primary_key=True
    )

    record = db.relationship(
        'Record',
        cascade="save-update, merge, delete"
    )

    tag = db.relationship(
        'Tag',
        cascade="save-update, merge, delete"
    )
