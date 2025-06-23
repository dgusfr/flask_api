from flask import Flask, request

app = Flask(__name__)

store = [
    {
        "name": "My Store",
        "items": [
            {"name": "My Item", "price": 15.99},
            {"name": "Another Item", "price": 9.99},
        ],
    }
]


@app.get("/store")
def get_stores():
    return {"stores": store}

@app.post("/store")
def create_store():
    
