from flask import jsonify, Blueprint, current_app, Response

bp = Blueprint('ping', __name__)

@bp.route('', methods=['GET'])
def ping():
    return jsonify({'code': 'ping success'})
