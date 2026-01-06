from functools import wraps
from flask import request, jsonify, current_app
import jwt


def token_required(f):
    @wraps
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            try:
                token = request.headers["Authorization"].split(" ")[1]
            except IndexError:
                return jsonify({"message": "Token format is invalid!"}), 401
        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            jwt.decode(token, current_app.config["SECRET_KEY"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid!"}), 401
