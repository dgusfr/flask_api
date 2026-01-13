from flask import Blueprint, jsonify, request
from app import db
from app.models.products import Product, ProductDBModel
from app.models.sales import Sales
from app.decorators import token_required
from bson.objectid import ObjectId
from pydantic import ValidationError
import csv
import io
from flasgger import swag_from

products_bp = Blueprint("products", __name__)


@products_bp.route("/products", methods=["GET"])
@swag_from("../../docs/products/get_products.yml")
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
@swag_from("../../docs/products/create_product.yml")
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
@swag_from("../../docs/products/get_product_by_id.yml")
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
@swag_from("../../docs/products/update_product.yml")
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
@swag_from("../../docs/products/delete_product.yml")
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
@swag_from("../../docs/products/upload_sales.yml")
def upload_sales(token):
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files["file"]

    if not file.filename:
        return jsonify({"error": "Nenhum arquivo selecionado"}), 400

    if not file.filename.endswith(".csv"):
        return jsonify({"error": "O arquivo deve ser um CSV"}), 400

    try:
        stream = io.StringIO(file.stream.read().decode("UTF-8"), newline=None)
        csv_reader = csv.DictReader(stream)

        sales_to_insert = []
        errors = []

        for row_num, row in enumerate(csv_reader, start=1):
            try:
                sale_data = Sales.model_validate(row)
                sales_to_insert.append(sale_data.model_dump())
            except ValidationError as e:
                errors.append(f"Linha {row_num}: Dados inválidos - {e.errors()}")
            except Exception as e:
                errors.append(f"Linha {row_num}: Erro inesperado - {str(e)}")

        if sales_to_insert:
            try:
                db.sales.insert_many(sales_to_insert)
            except Exception as e:
                return (
                    jsonify({"error": f"Erro crítico ao salvar no banco: {str(e)}"}),
                    500,
                )

        return (
            jsonify(
                {
                    "message": "Processamento concluído",
                    "vendas_importadas": len(sales_to_insert),
                    "total_erros": len(errors),
                    "detalhes_erros": errors,
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": f"Erro ao processar o arquivo: {str(e)}"}), 500
