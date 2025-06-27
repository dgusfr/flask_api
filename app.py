from flask import Flask, request

app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {"stores": store}


@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {
        "name": request_data["name"],
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


@app.get("/store/<string:name>")
def get_store(name):
    for s in store:
        if s["name"] == name:
            return {"store": s}
    return {"message": "Store not found"}, 404.0


@app.get("/store/<string:name>/item")
def get_items_in_store(name):
    for s in store:
        if s["name"] == name:
            return {"store": s["items"]}
    return {"message": "Store not found"}, 404
