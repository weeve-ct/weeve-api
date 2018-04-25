from flask import jsonify, Blueprint, request, current_app
import time
import socket
import logging
from server.controller import helpers

logger = logging.getLogger(__name__)
bp = Blueprint('health', __name__)

@bp.route('/', methods=['GET'])
def healthcheck():
    logger.debug('health check')
    return jsonify({
        'code':'alive',
        'host': socket.gethostname(),
        'uptime': round(helpers.get_uptime(),2)
    })
