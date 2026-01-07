from flask import Blueprint, jsonify, request
from app import db
from app.models.products import Product, ProductDBModel
from app.decorators import token_required
from bson.objectid import ObjectId
from pydantic import ValidationError

products_bp = Blueprint("products", __name__)


@products_bp.route("/products", methods=["GET"])
def get_products():
    products_cursor = db.products.find({})
    products_list = []
    for product in products_cursor:
        try:
            products_list.append(
                ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True)
            )
        except ValidationError:
            continue
    return jsonify(products_list), 200


@products_bp.route("/products", methods=["POST"])
@token_required
def create_products(token):
    try:
        raw_data = request.get_json()
        product = Product(**raw_data)
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
    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400
    except Exception:
        return jsonify({"message": "Error processing data"}), 500


@products_bp.route("/products/<string:product_id>", methods=["GET"])
def get_product(product_id):
    try:
        oid = ObjectId(product_id)
        product = db.products.find_one({"_id": oid})
        if not product:
            return jsonify({"message": "Product not found"}), 404
        return jsonify(ProductDBModel(**product).model_dump(by_alias=True)), 200
    except Exception:
        return jsonify({"message": "Invalid ID format"}), 400


@products_bp.route("/products/<string:product_id>", methods=["PUT"])
@token_required
def update_product(token, product_id):
    try:
        oid = ObjectId(product_id)
    except Exception:
        return jsonify({"message": "Invalid ID format"}), 400

    update_payload = request.get_json()
    if not update_payload:
        return jsonify({"message": "No input data provided"}), 400

    result = db.products.update_one({"_id": oid}, {"$set": update_payload})

    if result.matched_count == 0:
        return jsonify({"message": "Product not found"}), 404

    updated_product = db.products.find_one({"_id": oid})
    if updated_product:
        response_model = ProductDBModel(**updated_product)
        return jsonify(response_model.model_dump(by_alias=True)), 200

    return jsonify({"message": "Product not found"}), 404


@products_bp.route("/products/<string:product_id>", methods=["DELETE"])
@token_required
def delete_product(token, product_id):
    try:
        oid = ObjectId(product_id)
    except Exception:
        return jsonify({"message": "Invalid ID format"}), 400

    result = db.products.delete_one({"_id": oid})

    if result.deleted_count == 1:
        return jsonify({"message": "Product deleted successfully"}), 200
    else:
        return jsonify({"message": "Product not found"}), 404


@products_bp.route("/sales/upload", methods=["POST"])
@token_required
def upload_sales(token):
    return jsonify({"message": "Upload sales data"}), 200
