import datetime
from server.models import db


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    title = db.Column(db.String(30), primary_key=False, unique=False, nullable=False)
    body = db.Column(db.Text, primary_key=False, unique=False, nullable=False)

    post_tags = db.relationship('PostTag')
    collaborators = db.relationship('User', secondary='post_user')
    upvotes = db.relationship('User', secondary='post_upvote_user')

class PostUser(db.Model):
    __tablename__ = 'post_user'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    # relationships
    user = db.relationship('User', cascade="save-update, merge, delete")
    post = db.relationship('Post', cascade="save-update, merge, delete")

class PostTag(db.Model):
    # http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html#association-object
    __tablename__ = 'post_tag'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    is_explicit = db.Column(db.Boolean, nullable=False, default=True)

    post = db.relationship('Post', cascade="save-update, merge, delete")
    tag = db.relationship('Tag', cascade="save-update, merge, delete")

class PostUpvoteUser(db.Model):
    __tablename__ = 'post_upvote_user'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    post = db.relationship('Post', cascade="save-update, merge, delete")
    user = db.relationship('User', cascade="save-update, merge, delete")
