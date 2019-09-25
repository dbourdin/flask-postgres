import logging
import pathlib
import signal
import sys

import logbook
from flask import Blueprint
from flask import Flask
from flask_cors import CORS
from gevent.pywsgi import LoggingLogAdapter
from gevent.pywsgi import WSGIServer
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists

import config
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


# Create log directory
pathlib.Path(config.LOG_PATH).mkdir(parents=True, exist_ok=True)

logbook.StreamHandler(sys.stdout).push_application()
logbook.RotatingFileHandler(config.LOGFILE, max_size=52428800,
                            bubble=True).push_application()
logbook.compat.redirect_logging(set_root_logger_level=False)
logging.root.setLevel(config.LOGLEVEL)

logger = logbook.Logger('[SERVER]', getattr(logbook, config.LOGLEVEL))

app = Flask('flask')
users_blueprint = Blueprint('users', __name__, url_prefix='/users')
app.register_blueprint(users_blueprint)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_CONNECTION_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

wsgi_logger = LoggingLogAdapter(logging.getLogger('wsgi'), level=logging.DEBUG)
wsgi_server = WSGIServer((config.API_IP, config.API_PORT), app,
                         log=wsgi_logger, error_log=wsgi_logger)


def _create_db():
    if not database_exists(config.DB_CONNECTION_STRING):
        logger.debug('DB does not exist... Creating DB')
        create_database(config.DB_CONNECTION_STRING)
        logger.debug('DB created')


def _register_signal_handler():
    signal.signal(signal.SIGINT, signal_handler)
    signal.siginterrupt(signal.SIGINT, False)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.siginterrupt(signal.SIGTERM, False)


def signal_handler(signal, frame):
    logger.info('Exiting...')
    wsgi_server.stop()


def start_server():
    logger.info('Initializing DB')
    _create_db()
    db.create_all()
    logger.info('DB initialized')
    logger.info('Started')
    _register_signal_handler()
    wsgi_server.serve_forever()
    logger.info('Exited')
