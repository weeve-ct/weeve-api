import logging
from flask import request, jsonify
from server.models import db, Tag
from server.controller import helpers
from server.controller.security import SecureBlueprint
from server.controller.errors import ValidationError, QueryError

logger = logging.getLogger(__name__)
bp = SecureBlueprint('tag', __name__)

@bp.route('/', methods=['GET'])
@bp.route('/<id>', methods=['GET'])
def get_tag(tag_id=None):

    # single tag
    if tag_id is not None:
        tag = db.session.query(Tag).filter_by(id=tag_id).first()
        QueryError.raise_assert(tag is not None, 'tag_id <{}> not found'.format(tag_id))

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
    include_implicit = helpers.make_boolean(request.args.get('implicit').lower())
    if helpers.make_boolean(request.args.get('implicit').lower()):
        # filter out implicit tags
        q = q.filter(Tag.has_explicit == True)

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
