import logbook

from server import users_blueprint

import config
# from models import User

logger = logbook.Logger('[API]', getattr(logbook, config.LOGLEVEL))


#
# @users_blueprint.route('/', methods=['POST'])
# def create_user():
