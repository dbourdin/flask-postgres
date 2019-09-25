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
    errors = user_schema.validate(user_data)
    if errors:
        return jsonify(errors), 400
    new_user = User.create_user(**user_data)
    if not new_user:
        return jsonify(f'User {user_data["name"]} could not be created'), 400
    return user_schema.jsonify(new_user), 201


@users_blueprint.route('/', methods=['GET'])
def list_users():
    return jsonify(users_schema.dump(User.query.all()))


@users_blueprint.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    if type(user_id) != int:
        return jsonify(f'Invalid user id: {user_id}'), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify(f'User with id {user_id} does not exist'), 404
    return user_schema.jsonify(User.query.get(user_id))


@users_blueprint.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    user.update_user(**request.json)
    return user_schema.jsonify(user)


@users_blueprint.route('/<id>', methods=['DELETE'])
def delete_user(user_id):
    User.delete_user(user_id)
    return jsonify(), 204
