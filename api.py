import logbook
from flask import Blueprint

import config

logger = logbook.Logger('[API]', getattr(logbook, config.LOGLEVEL))

blueprint = Blueprint('api', __name__)
