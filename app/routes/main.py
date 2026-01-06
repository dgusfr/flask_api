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
        raw_data = request.get_json()
        user_data = LoginPayload(**raw_data)
    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400
    except Exception as e:
        return jsonify({"message": "Error processing data"}), 500

    if user_data.username == "admin" and user_data.password == "supersecret":
        payload = {
            "user_id": user_data.username,
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1),
        }

        token_gerado = jwt.encode(
            payload, current_app.config["SECRET_KEY"], algorithm="HS256"
        )

        return jsonify({"access_token": token_gerado}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


# Criação de produto
@main_bp.route("/products", methods=["POST"])
@token_required
def create_products(token):
    try:
        product = Product(**request.get_json())
    except Exception as e:
        return jsonify({"message": "Error processing data"}), 500

    result = db.products.insert_one(
        product.model_dump(by_alias=True, exclude_none=True)
    )
    return (
        jsonify(
            {
                "message": f"Add a new product by user {token.get('user_id')} with id {result.inserted_id}"
            }
        ),
        201,
    )


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
@token_required
def update_product(token, product_id):
    try:
        update_data = request.get_json()
        db.products.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data},
        )
    except Exception as e:
        return jsonify({"message": f"Error updating product {product_id}: {e}"}), 500
    return jsonify({"message": f"Update product {product_id}"})


# Exclusão/Venda de produto
@main_bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    return jsonify({"message": f"Delete product {product_id}"})


# Importar de vendas
@main_bp.route("/sales/upload", methods=["POST"])
def upload_sales():
    return jsonify({"message": "Upload sales data"})
