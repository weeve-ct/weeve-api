import logging
from flask import request, jsonify, g
from server.models import db, User
from server.controller.security import SecureBlueprint
from server.controller.errors import ValidationError, QueryError, NotImplementedError

logger = logging.getLogger(__name__)
bp = SecureBlueprint('user', __name__)

@bp.route('/', methods=['GET'])
@bp.route('/<int:user_id>', methods=['GET'])
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

@bp.route('/<int:user_id>', methods=['PUT', 'PATCH'])
def edit_user(user_id):
    ValidationError.raise_assert(request.json, 'missing request json')

    body = request.json

    user = db.session.query(User).filter_by(id=user_id).first()
    QueryError.raise_assert(user is not None, 'user "{}" not found'.format(user_id))

    # check that body user matches url user
    if 'user_id' in request.json:
        ValidationError.raise_assert(body['user_id']==user_id, \
        'payload user_id different from url')

    # check that token user == url user
    if g['current_user'].user_id != user_id:
        raise PermissionsError('not authorized to edit this user')

    if 'username' in body:
        user.username = body['username']

    if 'display_name' in body:
        user.display_name = body['display_name']

    output = {
        'user_id': user.id,
        'username': user.username,
        'display_name': user.display_name,
        'picture': user.picture,
    }
    return jsonify({'user': output})

@bp.route('/<int:user_id>/picture/', methods=['GET'])
def get_user_picture(user_id):
    '''get user picture'''
    raise NotImplementedError()

@bp.route('/<int:user_id>/picture/', methods=['PUT'])
def set_user_picture(user_id):
    '''set user picture'''
    raise NotImplementedError()
