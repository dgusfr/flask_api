from flask import Flask
from pymongo import MongoClient
import os


db = None


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

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
