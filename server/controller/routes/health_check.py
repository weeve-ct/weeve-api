from flask import jsonify, Blueprint, request, current_app
import time
import socket
from server.controller import helpers

bp = Blueprint('health', __name__)

@bp.route('/', methods=['GET'])
def healthcheck():
    return jsonify({
        'code':'alive',
        'host': socket.gethostname(),
        'uptime': round(helpers.get_uptime(),2)
    })
