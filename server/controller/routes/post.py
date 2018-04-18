import logging
from flask import request, jsonify
from server.models import db, Post, Tag, User
from server.controller.security import SecureBlueprint
from server.controller.errors import ValidationError, QueryError, NotImplementedError


logger = logging.getLogger(__name__)
bp = SecureBlueprint('post', __name__)


@bp.route('/', methods=['GET'])
@bp.route('/<post_id:int>', methods=['GET'])
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

    # validate payload
    assert payload is not None, 'missing json body'
    for required_field in ['title','body','collaborators','tags']:
        ValidationError.raise_assert(
            bool=required_field in payload,
            msg='"{}" required'.format(required_field)
        )

    post = Post(
        title=payload['title'],
        body=payload['body']
    )

    # get/create tags
    for tag_name in payload['tags']:
        tag = db.session.query(Tag).filter_by(tag=tag_name)
        if tag is None:
            tag = Tag(tag=tag_name)
            db.session.add(tag)

        post.tags.append(tag)

    # add collaborators
    # TODO: allow mixed types (users & teams)
    for user_id in payload['collaborators']:
        pass

    db.session.add(post)
    db.session.commit()

    output = {}

    return jsonify({'post':output}), 201

@bp.route('/<post_id:int>', methods=['PUT', 'PATCH'])
def edit_post(post_id):
    pass
