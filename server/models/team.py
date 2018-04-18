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

    def set_password(self, password):
        '''hash via bcrypt and persist to user'''

        self.hashed_password = bcrypt.hashpw(
            password=password.encode('utf-8'),
            salt=bcrypt.gensalt()
        )

    def check_password(self, password):
        '''check password against hashed user pwd using bcrypt'''

        return bcrypt.checkpw(
            password=password.encode('utf-8'),
            hashed_password=self.hashed_password
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
