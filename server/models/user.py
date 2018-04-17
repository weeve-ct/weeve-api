import bcrypt, datetime
from server.models import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), primary_key=False, unique=True, nullable=False)
    hashed_password = db.Column(db.String(64), nullable=False)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    last_login_date = db.Column(db.DateTime, nullable=True)
    minimum_iat = db.Column(db.Numeric, nullable=False)

    # posts = db.relationship('Post')

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
