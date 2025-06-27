from flask import Flask, request
from db import items, stores
import uuid

app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
    try:
        store_data = request.get_json()
        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores.stores[store_id] = store
        return {"store": store}, 201
    except KeyError:
        return {"message": "Invalid store data"}, 400


@app.post("/item")
def create_item(name):
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item


@app.get("/store/<string: store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "Store not found"}, 404


@app.get("/store/<string:name>/item")
def get_items_in_store(name):
    for s in store:
        if s["name"] == name:
            return {"store": s["items"]}
    return {"message": "Store not found"}, 404
