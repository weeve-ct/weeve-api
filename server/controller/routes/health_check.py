from flask import jsonify, Blueprint, request, current_app
import time
import socket

bp = Blueprint('health', __name__)

@bp.route('/', methods=['GET', 'POST'])
def healthcheck():
    return jsonify({
        'code':'alive',
        'host': socket.gethostname(),
        'uptime': round(time.time() - current_app.config['APP_START_TIME'],2)
    })
