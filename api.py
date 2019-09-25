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


@users_blueprint.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id,
                                 f'User with id {user_id} does not exist')
    return user_schema.jsonify(user)


@users_blueprint.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id,
                                 f'User with id {user_id} does not exist')
    user.update_user(**request.json)
    return user_schema.jsonify(user)


@users_blueprint.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not User.delete_user(user_id):
        return jsonify(f'Could not delete user {user_id}'), 400
    return jsonify(), 204
