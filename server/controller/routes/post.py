import logging
from flask import request, jsonify, g
from itertools import chain
from server.models import db, Post, Tag, User, PostTag
from server.controller.security import SecureBlueprint
from server.controller.errors import ValidationError, QueryError, NotImplementedError
from server.controller.tokenizer import title_tokenizer, get_insensitive_unique, clean_whitespace


logger = logging.getLogger(__name__)
bp = SecureBlueprint('post', __name__)


@bp.route('/', methods=['GET'])
@bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id=None):
    if not post_id is None:
        post = db.session.query(Post).filter_by(id=post_id).first()
        QueryError.raise_assert(post is not None, 'post "{}" not found'.format(post_id))

        output = {
            'post_id': post.id,
            'created_date': post.created_date,
            'modified_date': post.modified_date,
            'title': post.title,
            'body': post.body,
            'collaborators': [user.id for user in post.collaborators],
            'upvotes': [user.id for user in post.upvotes],
            'explicit_tags': [],
            'implicit_tags': [],
        }

        for post_tag in post.post_tags:
            if post_tag.is_explicit:
                output['explicit_tags'].append(post_tag.tag.tag)
            else:
                output['implicit_tags'].append(post_tag.tag.tag)

        return jsonify({'post': output})
    else:
        raise NotImplementedError('GET for multiple posts not implemented yet')


@bp.route('/', methods=['POST'])
def create_post():

    payload = request.json

    logger.debug('validating request body')

    # validate payload
    assert payload is not None, 'missing json body'
    for required_field in ['title','body','collaborators','explicit_tags']:
        ValidationError.raise_assert(
            bool=required_field in payload,
            msg='"{}" required'.format(required_field)
        )

    logger.debug('create Post object')

    # init Post object
    post = Post(
        title=payload['title'],
        body=payload['body']
    )

    logger.debug('process tags')

    # get implicit tags
    explicit_tag_names = map(clean_whitespace, payload['explicit_tags'])
    explicit_tag_names = map(lambda x: (x, True), explicit_tag_names)

    # compute implicit tags from title
    implicit_tag_names = map(clean_whitespace, title_tokenizer(post.title))
    implicit_tag_names = map(lambda x: (x, False), implicit_tag_names)

    known_tags = set()

    logger.debug('get/create tag objects')
    for (tag_name, is_explicit) in chain(explicit_tag_names, implicit_tag_names):
        tag_key = tag_name.strip().lower()

        if tag_key in known_tags:
            continue

        known_tags.add(tag_key)

        tag = db.session.query(Tag).filter(db.func.lower(Tag.tag)==db.func.lower(tag_name)).first()

        # allow on-the-fly tag creation
        if tag is None:
            tag = Tag(tag=tag_name, has_explicit=is_explicit)
            db.session.add(tag)
        else:
            if is_explicit and tag.has_explicit==False:
                tag.has_explicit = True
                db.session.add(tag)

        post_tag = PostTag(is_explicit=is_explicit)
        post_tag.tag = tag
        post.post_tags.append(post_tag)

    # add collaborators
    # TODO: allow mixed types (users & teams)
    logger.debug('get collaborators')
    for user_id in payload['collaborators']:
        user = db.session.query(User).filter_by(id=user_id).first()
        QueryError.raise_assert(user is not None, 'user "{}" not found'.format(user_id))
        post.collaborators.append(user)

    if g.current_user not in post.collaborators:
        post.collaborators.append(g.current_user)

    logger.debug('persist Post object to db')

    db.session.add(post)
    db.session.commit()

    output = {
        'post_id': post.id,
        'title': post.title,
        'body': post.body,
        'created_date': post.created_date,
        'modified_date': post.modified_date,
        'explicit_tags': [],
        'implicit_tags': [],
        'collaborators': [user.id for user in post.collaborators],
        'upvotes': [user.id for user in post.upvotes],
    }

    for post_tag in post.post_tags:
        if post_tag.is_explicit:
            output['explicit_tags'].append(post_tag.tag.tag)
        else:
            output['implicit_tags'].append(post_tag.tag.tag)

    return jsonify({'post':output}), 201

@bp.route('/<int:post_id>', methods=['PUT', 'PATCH'])
def edit_post(post_id=None):
    raise NotImplementedError()

    post = db.session.query(Post).filter_by(id=post_id).first()
    QueryError.raise_assert(post is not None, 'post "{}" not found'.format(post_id))

    post.modified_date = datetime.datetime.now()

    db.session.add(post)
    db.session.commit()


@bp.route('/<int:post_id>/upvote/', methods=['POST','PUT'])
def create_post_upvote(post_id):

    post = db.session.query(Post).filter_by(id=post_id).first()
    QueryError.raise_assert(post is not None, 'post "{}" not found'.format(post_id))

    if g.current_user not in post.upvotes:
        post.upvotes.append(g.current_user)
        db.session.add(post)
        db.session.commit()
        logger.debug('user "{}" upvoted post "{}"'.format(g.current_user.id, post.id))

    return jsonify({'code': 'success'})


@bp.route('/<int:post_id>/upvote/', methods=['DELETE'])
def delete_post_upvote(post_id):
    post = db.session.query(Post).filter_by(id=post_id).first()
    QueryError.raise_assert(post is not None, 'post "{}" not found'.format(post_id))

    if g.current_user in post.upvotes:
        post.upvotes.remove(g.current_user)
        db.session.add(post)
        db.session.commit()
        logger.debug('user "{}" delete upvote post "{}"'.format(g.current_user.id, post.id))

    return jsonify({'code': 'success'})
