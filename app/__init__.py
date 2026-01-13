from flask import Flask
from pymongo import MongoClient
from flasgger import Swagger
import os


db = None


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs",
        "openapi": "3.0.0",
    }

    template = {
        "swagger": "2.0",
        "info": {
            "title": "API E-commerce",
            "description": "API para gerenciamento de produtos, usuários e vendas.",
            "version": "1.0.0",
        },
        "components": {
            "securitySchemes": {
                "Bearer": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Insira seu token JWT no formato: Bearer <seu_token>",
                }
            }
        },
        "security": [{"Bearer": []}],
    }

    Swagger(app, config=swagger_config, template=template)

    global db

    try:
        client = MongoClient(app.config["MONGO_URI"])
        db = client.get_default_database()
    except Exception as e:
        print(f"Erro na conexão de Banco de Dados: {e}")

    from .routes.auth import auth_bp
    from .routes.products import products_bp
    from .routes.users import user_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)

    return app
