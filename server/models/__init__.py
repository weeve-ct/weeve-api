from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .tag import Tag
from .post import Post, PostUser, PostTag
from .team import Team, UserTeam
