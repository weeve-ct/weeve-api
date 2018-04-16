from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .tag import Tag
from .record import Record
