import logging
from flask import request, jsonify, g
from server.models import db, Post, Tag, User, PostTag, PostUser
from server.controller.security import SecureBlueprint
from server.controller.errors import *
from server.controller.tokenizer import get_tokens

logger = logging.getLogger(__name__)
bp = SecureBlueprint('search', __name__)

@bp.route('/post/', methods=['POST'])
def search():
    logger.debug('validating request body')

    # validate payload
    payload = request.json
    assert payload is not None, 'missing json body'

    ValidationError.raise_assert('keywords' in payload, 'missing keywords')
    ValidationError.raise_assert('collaborators' in payload, 'missing collaborators')

    logger.debug('begin search')
    keywords = payload['keywords']
    collaborator_ids = payload.get('collaborators', [])

    # tokenize the search keywords
    logger.debug('tokenize search keywords')

    tokens = get_tokens(keywords)

    # identify direct tags in the keywords string
    original_words = set(t['original'].lower() for t in tokens if t['original']!=t['output'])
    q = db.session.query(Tag)
    q = q.filter(db.func.lower(Tag.tag).in_(original_words))
    tags = q.all()

    reverse_tag_lookup = {tag.tag.lower(): tag for tag in tags}

    add_tokens = []
    for token in tokens:
        if token['original'] in reverse_tag_lookup and token['original'] != token['output']:
            tag_obj = reverse_tag_lookup[token['original']]
            add_tokens.append(
                {
                    'output': tag_obj.tag,
                    'tag_id': tag_obj.id
                }
            )
    if add_tokens:
        logger.debug('found direct tags: {}'.format([t['output'] for t in add_tokens]))
        tokens.extend(add_tokens)

    search_tags = set([t['output'] for t in tokens if not t.get('ignore')])

    logger.debug('searching with tags: {}'.format(search_tags))

    q = db.session.query(Post, db.func.count(Tag.tag))
    q = q.select_from(Post)
    q = q.join(Post.post_tags)
    q = q.join(PostTag.tag)

    if collaborator_ids:
        logger.debug('filtering to users: {}'.format(collaborator_ids))
        q = q.join(PostUser)
        q = q.join(User)
        q = q.filter(User.id.in_(collaborator_ids))

    q = q.filter(Tag.tag.in_(search_tags))
    q = q.group_by(Post)
    q = q.having(db.func.count(Tag.tag) >= 1)

    results = q.all()

    logger.debug('found {} results'.format(len(results)))

    output = []
    for r in results:
        post, count = r
        explicit_tags = [p.tag.tag.lower() for p in post.post_tags if p.tag.has_explicit==True]
        upvotes = len(post.upvotes)
        explicit_tags.sort()

        output_record = {
            'post_id': post.id,
            'title': post.title,
            'explicit_tags': explicit_tags,
            'upvotes': upvotes,
            'modified_date': post.modified_date,
        }

        sort_key = (count, upvotes, int(post.modified_date.timestamp()))

        output.append((sort_key, output_record))

    logger.debug('black magic sorting')
    output.sort(key=lambda x: x[0], reverse=True)
    output = [o[1] for o in output]

    return jsonify({'posts': output})

    # find the users
