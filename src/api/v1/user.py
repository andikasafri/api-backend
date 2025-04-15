from flask import jsonify, request
from ...models.user import User
from ...utils.auth import token_required
from . import api_v1

@api_v1.route("/users", methods=["GET"])
@token_required
def get_users(current_user):
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@api_v1.route("/profile", methods=["GET"])
@token_required
def get_profile(current_user):
    return jsonify(current_user.to_dict())
