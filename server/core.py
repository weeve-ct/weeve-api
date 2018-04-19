import logging
import os
import yaml
import time
from flask import Flask
from .models import db
from .controller import routes, helpers, errors

logger = logging.getLogger(__name__)

def create_app(debug=False, raise_errors=False):
    app = Flask(__name__)

    # set debug mode
    app.debug = debug

    # raise app errors
    app.config['RAISE_ERRORS'] = raise_errors

    # register default encoder
    app.json_encoder = helpers.JSONEncoder

    # register error handler
    errors.register_error_handlers(app)

    # configure logging
    configure_logging(debug=debug)

    # configure app
    configure_flask(app=app)

    # bind database
    db.init_app(app)

    # register blueprints
    app.register_blueprint(routes.health_check.bp, url_prefix='')
    app.register_blueprint(routes.auth.bp, url_prefix='/auth')
    app.register_blueprint(routes.team.bp, url_prefix='/team')
    app.register_blueprint(routes.tag.bp, url_prefix='/tag')
    app.register_blueprint(routes.post.bp, url_prefix='/post')

    return app


def configure_flask(app):
    assert 'FLASK_CONFIG' in os.environ, 'missing FLASK_CONFIG in environment'
    fp = os.environ.get('FLASK_CONFIG')

    assert os.path.exists(fp), 'CANNOT FIND FLASK CONFIG "{fp}"'.format(fp=fp)

    # assert, 'bad flask config "fp"'
    logger.debug('reading config "{fp}"'.format(fp=fp))

    with open(fp, 'r') as f:
        conf_obj = yaml.load(f)

    app.config['AUTH_TOKEN_EXP'] = conf_obj.get('token_exp') or 60*60*24
    app.config['APP_START_TIME'] = time.time()
    app.config['SECRET_KEY'] = conf_obj['secret_key']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['EXTERNAL_URL'] = conf_obj['external_url']
    app.config['SQLALCHEMY_DATABASE_URI'] = conf_obj['db']['url']


def configure_logging(debug=False):
    root = logging.getLogger()
    h = logging.StreamHandler()
    fmt = logging.Formatter(
        fmt='%(asctime)s %(levelname)s (%(name)s) %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S'
    )
    h.setFormatter(fmt)
    root.addHandler(h)

    if debug:
        root.setLevel(logging.DEBUG)
    else:
        root.setLevel(logging.INFO)


def create_tables():
    app = create_app()
    with app.app_context():
        db.create_all()


def reset_db():
    app = create_app()
    with app.app_context():
        logger.info('dropping tables')
        db.drop_all()
        logger.info('creating tables')
        db.create_all()
