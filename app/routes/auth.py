from flask import Blueprint, jsonify, request, current_app
from app.models.user import LoginPayload
from pydantic import ValidationError
import jwt
from datetime import datetime, timedelta, timezone

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Bem-vindo à API Flask!"})


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        raw_data = request.get_json()
        user_data = LoginPayload(**raw_data)
    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400
    except Exception:
        return jsonify({"message": "Erro ao processar dados"}), 500

    # Lógica de validação (Simulada - idealmente buscaria do banco de usuários)
    if user_data.username == "admin" and user_data.password == "1234":
        payload = {
            "user_id": user_data.username,
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1),
        }

        token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
        return jsonify({"access_token": token}), 200
    else:
        return jsonify({"message": "Credenciais inválidas"}), 401
