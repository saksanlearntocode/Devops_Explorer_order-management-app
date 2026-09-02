from pymongo import MongoClient
import os

host = os.getenv("MONGO_HOST", "mongodb-svc")
port = int(os.getenv("MONGO_PORT", "27017"))
db_name = os.getenv("MONGO_DB", "ordersdb")

client = MongoClient(f"mongodb://{host}:{port}/")
db = client[db_name]

orders = db.orders.find({"status": "pending"})

count = 0

for order in orders:
    print(f"Processing order: {order['id']}")

    db.orders.update_one(
        {"_id": order["_id"]},
        {"$set": {"status": "processed"}}
    )

    count += 1

print(f"Processed {count} orders")