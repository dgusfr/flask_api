from flask import Flask
from .routes.main import main_bp
from pymongo import MongoClient


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.config.from_object("config.Config")
    global db

    try:
        client = MongoClient(app.config["MONGO_URI"])
        db = client.get_default_database()
    except Exception as e:
        print("Erro na conexão de Banco de Dados.")

    return app
