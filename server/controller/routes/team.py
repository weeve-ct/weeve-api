from flask import request, jsonify
from server.models import db, Team
from server.controller.security import SecureBlueprint
from server.controller.errors import ValidationError, QueryError

bp = SecureBlueprint('team', __name__)

@bp.route('/', methods=['GET'])
@bp.route('/<id>', methods=['GET'])
def get_team(team_id=None):
    # get all teams
    if team_id is None:
        output = []

        for team in db.session.query(Team).all():
            output.append([
                {
                    'team_id': team.id,
                    'team_name': team.team_name,
                }
            ])

        return jsonify({'teams': output})

    # get single team
    else:
        team = db.session.query(Team).filter_by(id=team_id).first()

        if team is None:
            raise QueryError('team <{}> not found'.format(team_id))

        return jsonify(
            {
                'team_id': team.id,
                'team_name': team.team_name
            }
        )

@bp.route('/', methods=['POST'])
def create_team():
    payload = request.json

    # validate payload
    assert payload is not None, 'missing json body'
    ValidationError.raise_assert('team_name' in payload, 'team_name required')

    team_name = payload['team_name']

    # check duplicates
    duplicates = db.session.query(Team).filter_by(team_name=team_name).first()
    ValidationError.raise_assert(duplicates is None, 'team "{}" already exists'.format(team_name))

    new_team = Team(
        team_name=team_name,
    )

    db.session.add(new_team)
    db.session.commit()

    output = {
        'team_id': new_team.id,
        'team_name': new_team.team_name
    }

    return jsonify({'team': output}), 201
