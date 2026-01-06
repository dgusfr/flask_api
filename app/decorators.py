from functools import wraps
from flask import request, jsonify, current_app
import jwt


def token_required(funcao_protegida):
    @wraps(funcao_protegida)
    def decorador(*args, **kwargs):
        token = None
        header_autorizacao = request.headers.get("Authorization")

        if header_autorizacao:
            partes = header_autorizacao.split(" ")
            if len(partes) == 2:
                token = partes[1]

        if not token:
            return jsonify({"message": "Token ausente ou mal formatado!"}), 401

        try:
            chave_secreta = current_app.config["SECRET_KEY"]
            dados_usuario = jwt.decode(token, chave_secreta, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "O Token expirou!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token inválido!"}), 401

        return funcao_protegida(dados_usuario, *args, **kwargs)

    return decorador
