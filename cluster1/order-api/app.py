from flask import Flask, jsonify, request
from pymongo import MongoClient
import os, uuid, datetime

app = Flask(__name__)

mongo_host = os.getenv("MONGO_HOST", "mongodb-svc")
mongo_port = int(os.getenv("MONGO_PORT", 27017))
mongo_db = os.getenv("MONGO_DB", "ordersdb")

client = MongoClient(f"mongodb://{mongo_host}:{mongo_port}/")
db = client[mongo_db]

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/orders", methods=["GET"])
def get_orders():
    orders = list(db.orders.find({}, {"_id": 0}))
    return jsonify(orders)

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.json
    order = {
        "id": str(uuid.uuid4()),
        "item": data.get("item"),
        "quantity": data.get("quantity"),
        "status": "pending",
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    db.orders.insert_one(order)
    order.pop("_id", None)
    return jsonify(order), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
