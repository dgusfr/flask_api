from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Flask API!"})


# Listagem de produtos
@main_bp.route("/products", methods=["GET"])
def products():
    return jsonify({"message": "List of Products"})


# Login de usuario
@main_bp.route("/login", methods=["POST"])
def login():
    return jsonify({"message": "LOGIN"})


# Criação de produto
@main_bp.route("/products", methods=["POST"])
def create_products():
    return jsonify({"message": "Add a new product"})


# Visualisação de produto
@main_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    return jsonify({"message": f"Details of product {product_id}"})


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
