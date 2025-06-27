from flask import Flask, request
from db import items, stores
import uuid

app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {
        "name": store_data["name"],
        "items": [],
    }
    store.append(new_store)
    return {"store": new_store}, 201


@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for s in store:
        if s["name"] == name:
            new_item = {
                "name": request_data["name"],
                "price": request_data["price"],
            }
            s["items"].append(new_item)
            return {"item": new_item}, 201
    return {"message": "Store not found"}, 404


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
