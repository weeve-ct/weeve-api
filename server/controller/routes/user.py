import logging
from flask import request, jsonify
from server.models import db, User
from server.controller.security import SecureBlueprint
from server.controller.errors import ValidationError, QueryError, NotImplementedError


logger = logging.getLogger(__name__)
bp = SecureBlueprint('tag', __name__)


@bp.route('/', methods=['GET'])
@bp.route('/<id>', methods=['GET'])
def get_user(user_id=None):
    # get single user
    if user_id is not None:
        user = db.session.query(User).filter_by(id=user_id).first()
        QueryError.raise_assert(user is not None, 'user "{}" not found'.format(user_id))
        output = {
            'user_id': user.id,
            'username': user.username,
            'display_name': user.display_name,
            'picture': user.picture,
        }
        return jsonify({'user': output})


@bp.route('/', methods=['PUT', 'PATCH'])
def edit_user():
    raise NotImplementedError('user edits not implemented yet')
