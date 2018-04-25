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
    logger.debug('logging in')
    logger.debug('validating request body')
    body = request.json
    assert body is not None, 'json missing'

    if 'username' not in body or 'password' not in body:
        raise errors.APIError('username and password required')

    username = body['username'].lower().strip()
    logger.debug('searching for user "{}"'.format(username))
    query = db.session.query(User).filter(db.func.lower(User.username)==username)
    user = query.first()

    errors.AuthError.raise_assert(user is not None) # check user exists

    logger.debug('checking password')
    errors.AuthError.raise_assert(user.check_password(body['password'])) # check password
    # errors.AuthError.raise_assert(u.is_verified, 'user not verified') # check verified

    logger.debug('updating last_login_date')
    user.last_login_date = datetime.datetime.now()
    db.session.add(user)
    db.session.commit()

    logger.debug('making token')
    # return session jwt
    token = security.make_expiring_jwt(
        payload={'username': user.username},
        exp=current_app.config['AUTH_TOKEN_EXP'],
    )

    return jsonify({'token': token}), 201

@bp.route('/signup', methods=['POST'])
def signup():
    logger.debug('begin user registration')

    logger.debug('validating request body')
    body = request.json
    errors.ValidationError.raise_assert(body is not None, 'json missing')
    if 'username' not in body or 'password' not in body:
        raise errors.APIError('username and password required')

    username = body['username'].lower().strip()
    logger.debug('searching for existing user "{}"'.format(username))
    query = db.session.query(User).filter(db.func.lower(User.username)==username)
    user = query.first()
    errors.AuthError.raise_assert(user is None, 'user already exists')

    logger.debug('creating new user')
    user = User(
        username = username,
        display_name = (body.get('display_name') or username)
    )

    logger.debug('setting password')
    user.set_password(body['password'])

    logger.debug('writing to db')
    db.session.add(user)
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

@bp.route('/check_token', methods=['GET','POST'])
@security.requires_auth
def check_token():
    '''check token sent as a auth header'''
    return jsonify({
        'token': g.current_token,
        'token_info': g.current_token_info,
        'user': g.current_user.username,
    })
