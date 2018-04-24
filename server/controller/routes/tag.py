import logging
from flask import request, jsonify
from server.models import db, Tag
from server.controller import helpers
from server.controller.security import SecureBlueprint
from server.controller.errors import ValidationError, QueryError

logger = logging.getLogger(__name__)
bp = SecureBlueprint('tag', __name__)

@bp.route('/', methods=['GET'])
@bp.route('/<tag_name>', methods=['GET'])
def get_tag(tag_name=None):

    # single tag
    if tag_name is not None:
        tag = db.session.query(Tag).filter(db.func.lower(Tag.tag)==db.func.lower(tag_name)).first()
        QueryError.raise_assert(tag is not None, 'tag <{}> not found'.format(tag_name))

        return jsonify({'tag': tag.tag})

    # multiple tags
    q = db.session.query(Tag)

    # apply "startswith" filter if passed via request args
    if 'startswith' in request.args.keys():
        QueryError.raise_assert(len(request.args.getlist('startswith'))<=1, 'can only specify startswith arg once')
        tag_prefix = request.args.get('startswith')
        q = q.filter(db.func.lower(Tag.tag).startswith(tag_prefix))
        logger.debug('filter tags starting with "{}"'.format(tag_prefix))

    # handle "implicit" filter
    QueryError.raise_assert(len(request.args.getlist('implicit'))<=1, 'can only specify implicit arg once')
    include_implicit = helpers.make_boolean(request.args.get('implicit',"false"))
    if not helpers.make_boolean(include_implicit):
        # filter out implicit tags
        q = q.filter(Tag.has_explicit == True)
        logger.debug('filter to only explicit tags')

    tags = q.all()
    output = [tag.tag for tag in tags]
    return jsonify({'tags': output})

@bp.route('/', methods=['POST'])
def create_tag():
    payload = request.json

    # validate payload
    assert payload is not None, 'missing json body'
    ValidationError.raise_assert('tag' in payload, 'tag required')

    tag_name = payload['tag']

    # check duplicates
    duplicates = db.session.query(Tag).filter_by(tag=tag_name).first()
    ValidationError.raise_assert(duplicates is None, 'tag "{}" already exists'.format(tag_name))

    tag = Tag(tag=tag_name)

    db.session.add(tag)
    db.session.commit()
    logger.debug('created tag "{}"'.format(tag.tag))

    return jsonify({'tag': {'tag_id': tag.id, 'tag': tag.tag}}), 201
