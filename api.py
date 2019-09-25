import logbook

from flask import Blueprint
from flask import request
from flask import jsonify


import config
from models import User
from models import UserSchema

users_blueprint = Blueprint('users', __name__, url_prefix='/users')

logger = logbook.Logger('[API]', getattr(logbook, config.LOGLEVEL))

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@users_blueprint.route('/', methods=['POST'])
def create_user():
    user_data = request.json
    new_user = User.create_user(**user_data)
    return user_schema.jsonify(new_user)


@users_blueprint.route('/', methods=['GET'])
def list_users():
    return jsonify(users_schema.dump(User.query.all()))


@users_blueprint.route('/<id>', methods=['GET'])
def get_user(id):
    return user_schema.jsonify(User.query.get(id))


@users_blueprint.route('/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    user.update_user(**request.json)
    return user_schema.jsonify(user)


@users_blueprint.route('/<id>', methods=['DELETE'])
def delete_user(id):
    User.delete_user(id)
    return jsonify(), 204
