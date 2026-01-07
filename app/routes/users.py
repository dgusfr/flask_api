from flask import Blueprint, jsonify, request
from app import db
from app.models.user import User, UserDBModel
from bson.objectid import ObjectId
from app.decorators import token_required

user_bp = Blueprint("users", __name__)


@user_bp.route("/users", methods=["GET"])
@token_required
def get_users(token):
    users_cursor = db.users.find({})
    users_list = [
        UserDBModel(**user).model_dump(by_alias=True, exclude={"password"})
        for user in users_cursor
    ]
    return jsonify(users_list), 200


@user_bp.route("/users", methods=["POST"])
def create_user():
    try:
        raw_data = request.get_json()
        new_user = User(**raw_data)

        if db.users.find_one({"username": new_user.username}):
            return jsonify({"message": "Username already exists"}), 409

        insert_result = db.users.insert_one(
            new_user.model_dump(exclude={"id"}, by_alias=True)
        )

        return (
            jsonify(
                {"message": f"User created with ID: {str(insert_result.inserted_id)}"}
            ),
            201,
        )

    except Exception as e:
        return jsonify({"message": f"Error creating user: {e}"}), 400


@user_bp.route("/users/<string:user_id>", methods=["DELETE"])
@token_required
def delete_user(token, user_id):
    try:
        oid = ObjectId(user_id)
        result = db.users.delete_one({"_id": oid})

        if result.deleted_count == 1:
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"message": "User not found"}), 404

    except Exception:
        return jsonify({"message": "Invalid ID format"}), 400
