import re
import datetime
import time
from urllib.parse import urljoin
from flask import jsonify, Blueprint, url_for, current_app, request, g
from server.controller import security, errors
from server.models import db, User
from flask import logging

bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@bp.route('/login', methods=['POST'])
def login():
    logger.info('logging in')

    body = request.json
    assert body is not None, 'json missing'

    if 'username' not in body or 'password' not in body:
        raise errors.APIError('username and password required')

    u = db.session.query(User).filter_by(username=body['username']).first()

    errors.AuthError.raise_assert(u is not None) # check user exists
    errors.AuthError.raise_assert(u.check_password(body['password'])) # check password
    # errors.AuthError.raise_assert(u.is_verified, 'user not verified') # check verified

    u.last_login_date = datetime.datetime.now()
    db.session.add(u)
    db.session.commit()

    # return session jwt
    token = security.make_expiring_jwt(
        payload={'username': u.username},
        exp=current_app.config['AUTH_TOKEN_EXP'],
    )

    return jsonify({'token': token})

@bp.route('/signup', methods=['POST'])
def signup():
    body = request.json
    print(body)

    if 'username' not in body or 'password' not in body:
        raise errors.APIError('username and password required')

    u = db.session.query(User).filter_by(username=body['username']).first()

    if not u is None:
        raise errors.AuthError('user already exists')

    u = User(
        username = body['username'],
        display_name = (body.get('display_name') or body['username'])
    )

    u.set_password(body['password'])

    db.session.add(u)
    db.session.commit()

    return jsonify({'code': 'success'})

@bp.route('/verify/<token>', methods=['GET', 'POST'])
def verify(token):
    try:
        payload = security.parse_url_token(token)
    except:
        raise errors.AuthError('bad token')

    if payload['exp'] < int(datetime.datetime.now().timestamp()):
        raise errors.AuthError('token expired')

    u = db.session.query(User).filter_by(username=payload['username']).first()
    errors.AuthError.raise_assert(u is not None) # check if user exists

    u.is_verified = True
    db.session.add(u)
    db.session.commit()

    return jsonify({'message': 'success'})

@bp.route('/check_token')
@security.requires_auth
def check_token():
    '''check token sent as a auth header'''
    return jsonify({
        'token': g.current_token,
        'token_info': g.current_token_info,
        'user': g.current_user.username,
    })
