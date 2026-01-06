from flask import Blueprint, jsonify, request, current_app
from app.models.user import LoginPayload
from pydantic import ValidationError
from app import db
from bson.objectid import ObjectId
from app.models.products import Product, ProductDBModel
from app.decorators import token_required
from datetime import datetime, timedelta, timezone
import jwt

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Flask API!"})


# Listagem de produtos
@main_bp.route("/products", methods=["GET"])
def products():
    products_cursor = db.products.find({})
    products_list = [
        ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True)
        for product in products_cursor
    ]
    return jsonify(products_list)


# Login de usuario
@main_bp.route("/login", methods=["POST"])
def login():
    try:
        raw_data = request.json()
        user_data = LoginPayload(**raw_data)
    except ValidationError as e:
        return jsonify({"message": e.errors()})
    except Exception as e:
        return jsonify({"message": "Error"}), 500
    if user_data.username == "admin" and user_data.password == "1234":
        jwt.encode(
            {
                "user_id": user_data.username,
                "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"})
    return jsonify({"message": "Login do usuario {user_data.model_dump_json}"})


# Criação de produto
@main_bp.route("/products", methods=["POST"])
def create_products():
    return jsonify({"message": "Add a new product"})


# Visualização de produto
@main_bp.route("/products/<string:product_id>", methods=["GET"])
def get_product(product_id):
    try:
        product = db.products.find_one({"_id": ObjectId(product_id)})

        if not product:
            return jsonify({"message": "Product not found"}), 404

        product["_id"] = str(product["_id"])
        return jsonify(product)

    except Exception as e:
        return jsonify({"message": f"Error retrieving product {product_id}: {e}"}), 500


# Atualização de produto
@main_bp.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    return jsonify({"message": f"Update product {product_id}"})


# Exclusão/Venda de produto
@main_bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    return jsonify({"message": f"Delete product {product_id}"})


# Importar de vendas
@main_bp.route("/sales/upload", methods=["POST"])
def upload_sales():
    return jsonify({"message": "Upload sales data"})
