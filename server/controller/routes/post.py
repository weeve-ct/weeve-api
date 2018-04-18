from flask import request, jsonify
from server.models import db, Post
from server.controller.security import SecureBlueprint
from server.controller.errors import ValidationError, QueryError
import logging

logger = logging.getLogger(__name__)

bp = SecureBlueprint('tag', __name__)

@bp.route('/', methods=['GET'])
@bp.route('/<id>', methods=['GET'])
def get_user(user_id=None):
    pass

@bp.route('/', methods=['PUT', 'PATCH'])
def edit_user():
    pass
