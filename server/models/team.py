import bcrypt, datetime
from server.models import db

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String(30), primary_key=False, unique=True, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    # posts = db.relationship('Post')
    users = db.relationship(
        'User',
        secondary='user_team'
    )

class UserTeam(db.Model):
    __tablename__ = 'user_team'

    user_id = db.Column(db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    )

    team_id = db.Column(db.Integer,
        db.ForeignKey('teams.id'),
        primary_key=True
    )

    user = db.relationship(
        'User',
        cascade="save-update, merge, delete"
    )

    team = db.relationship(
        'Team',
        cascade="save-update, merge, delete"

    )
