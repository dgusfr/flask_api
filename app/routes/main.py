from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Flask API!"})


@main_bp.route("/products", methods=["GET"])
def products():
    return jsonify({"message": "List of Products"})


@main_bp.route("/login", methods=["POST"])
def login():
    return jsonify({"message": "LOGIN"})
