import logbook
from flask import Blueprint

import config

logger = logbook.Logger('[API]', getattr(logbook, config.LOGLEVEL))

users_blueprint = Blueprint('users', __name__, url_prefix='/users')
