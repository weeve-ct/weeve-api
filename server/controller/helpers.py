from flask import current_app
from flask.json import JSONEncoder
import decimal, datetime, json
import time
from server.controller import errors

class JSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to floats
            return float(round(obj,2))
        elif isinstance(obj, (datetime.datetime,datetime.date,datetime.time)):
            return obj.isoformat()

        return super(JSONEncoder, self).default(obj)

def make_boolean(value):
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        value = value.strip().lower()
        if value in ('true','false'):
            return value == 'true'
        if value in ('1','0'):
            return value == '1'

    raise errors.ValidationError('could not parse boolean "{}"'.format(value))

def get_uptime():
    return time.time() - current_app.config['APP_START_TIME']
