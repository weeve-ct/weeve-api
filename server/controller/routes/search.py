import logging
from flask import request, jsonify, g
from server.models import db, Post, Tag, User, PostTag
from server.controller.security import SecureBlueprint
from server.controller.errors import *
from server.controller.tokenizer import get_tokens

logger = logging.getLogger(__name__)
bp = SecureBlueprint('search', __name__)

@bp.route('/', methods=['POST'])
def search():
    logger.debug('validating request body')

    # validate payload
    payload = request.json
    assert payload is not None, 'missing json body'

    logger.debug('begin search')

    # tokenize the search keywords
    keywords = payload['keywords']
    tokens = get_tokens(keywords)

    # find the users
