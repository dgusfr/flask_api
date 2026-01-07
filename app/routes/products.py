from flask import Blueprint, jsonify, request
from app import db
from app.models.products import ProductDBModel
from app.decorators import token_required
from bson.objectid import ObjectId
from pydantic import ValidationError

products_bp = Blueprint("products", __name__)


# --- Rotas Públicas (Exemplo: Listagem) ---
@products_bp.route("/products", methods=["GET"])
def get_products():
    products_cursor = db.products.find({})
    products_list = []

    for product in products_cursor:
        try:
            # Validamos cada produto para garantir que o JSON de saída esteja correto
            products_list.append(ProductDBModel(**product).model_dump(by_alias=True))
        except ValidationError:
            continue  # Pula produtos inconsistentes no banco

    return jsonify(products_list), 200


@products_bp.route("/products/<string:product_id>", methods=["GET"])
def get_product(product_id):
    try:
        oid = ObjectId(product_id)
        product = db.products.find_one({"_id": oid})

        if not product:
            return jsonify({"message": "Produto não encontrado"}), 404

        return jsonify(ProductDBModel(**product).model_dump(by_alias=True)), 200
    except Exception:
        return jsonify({"message": "ID inválido"}), 400


# --- Rotas Protegidas (Exigem Token) ---


@products_bp.route("/products", methods=["POST"])
@token_required
def create_product(token):
    # Aqui você implementaria a lógica real de inserir no banco
    # usando request.get_json() e o modelo Product
    return jsonify({"message": "Produto criado (simulação)"}), 201


@products_bp.route("/products/<string:product_id>", methods=["PUT"])
@token_required
def update_product(token, product_id):
    try:
        oid = ObjectId(product_id)
    except Exception:
        return jsonify({"message": "ID inválido"}), 400

    update_payload = request.get_json()
    if not update_payload:
        return jsonify({"message": "Sem dados para atualizar"}), 400

    result = db.products.update_one({"_id": oid}, {"$set": update_payload})

    if result.matched_count == 0:
        return jsonify({"message": "Produto não encontrado"}), 404

    updated_product = db.products.find_one({"_id": oid})
    if updated_product:
        return jsonify(ProductDBModel(**updated_product).model_dump(by_alias=True)), 200

    return jsonify({"message": "Erro ao recuperar produto atualizado"}), 500


@products_bp.route("/products/<string:product_id>", methods=["DELETE"])
@token_required
def delete_product(token, product_id):
    try:
        oid = ObjectId(product_id)
        result = db.products.delete_one({"_id": oid})

        if result.deleted_count == 1:
            return jsonify({"message": "Produto deletado com sucesso"}), 200
        else:
            return jsonify({"message": "Produto não encontrado"}), 404
    except Exception:
        return jsonify({"message": "ID inválido"}), 400


# Rota de Vendas (Mantida aqui para limpar o main.py)
@products_bp.route("/sales/upload", methods=["POST"])
@token_required
def upload_sales(token):
    return jsonify({"message": "Upload de vendas recebido"}), 200
