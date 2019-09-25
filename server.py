import logging
import pathlib
import signal
import sys

import logbook
from flask import jsonify
from gevent.pywsgi import LoggingLogAdapter
from gevent.pywsgi import WSGIServer
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists

import config
from api import users_blueprint
from app import app
from app import db

# Create log directory
pathlib.Path(config.LOG_PATH).mkdir(parents=True, exist_ok=True)

logbook.StreamHandler(sys.stdout).push_application()
logbook.RotatingFileHandler(config.LOGFILE, max_size=52428800,
                            bubble=True).push_application()
logbook.compat.redirect_logging(set_root_logger_level=False)
logging.root.setLevel(config.LOGLEVEL)

logger = logbook.Logger('[SERVER]', getattr(logbook, config.LOGLEVEL))

wsgi_logger = LoggingLogAdapter(logging.getLogger('wsgi'), level=logging.DEBUG)
wsgi_server = WSGIServer((config.API_IP, config.API_PORT), app,
                         log=wsgi_logger, error_log=wsgi_logger)

app.register_blueprint(users_blueprint)


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=500, text=str(e)), 500


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
