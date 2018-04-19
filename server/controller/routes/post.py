import logging
from flask import request, jsonify
from server.models import db, Post, Tag, User
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
            'title': post.title,
            'body': post.body,
            'collaborators': [],
            'tags': []
        }

        output['tags'] = [tag.tag for tag in post.tags]

        for user in post.collaborators:
            output['collaborators'].append(
                {
                    'user_id': user.id,
                    'username': user.username,
                    'display_name': user.display_name,
                }
            )

        return jsonify({'post': output})
    else:
        raise NotImplementedError('GET for multiple posts not implemented yet')

@bp.route('/', methods=['POST'])
def create_post():

    payload = request.json

    logger.debug('validating request body')

    # validate payload
    assert payload is not None, 'missing json body'
    for required_field in ['title','body','collaborators','tags']:
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

    # get tags
    tag_names = list(map(clean_whitespace, payload['tags']))

    # add title tags
    title_tags = title_tokenizer(post.title)

    # remove extra white space characters
    unique_tag_names = get_insensitive_unique(tag_names, title_tags)

    logger.debug('get/create tag objects')

    # get/create tags in db
    for tag_name in unique_tag_names:
        tag = db.session.query(Tag).filter(db.func.lower(Tag.tag)==db.func.lower(tag_name)).first()

        # allow on-the-fly tag creation
        if tag is None:
            tag = Tag(tag=tag_name)
            db.session.add(tag)

        post.tags.append(tag)

    logger.debug('get collaborators')

    # add collaborators
    # TODO: allow mixed types (users & teams)
    for user_id in payload['collaborators']:
        user = db.session.query(User).filter_by(id=user_id).first()
        QueryError.raise_assert(user is not None, 'user "{}" not found'.format(user_id))
        post.collaborators.append(user)

    logger.debug('persist Post object to db')

    db.session.add(post)
    db.session.commit()

    output = {
        'post_id': post.id,
        'title': post.title,
        'body': post.body,
        'tags': [tag.tag for tag in post.tags],
        'collaborators': [user.id for user in post.collaborators]
    }

    return jsonify({'post':output}), 201

@bp.route('/<int:post_id>', methods=['PUT', 'PATCH'])
def edit_post(post_id):
    pass
