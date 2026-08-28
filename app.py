from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://database-service:27017/")
db = client.byteburst
collection = db.catalog

if collection.count_documents({}) == 0:
    if collection.count_documents({}) == 0:
        collection.insert_many([
        {"id": 101, "name": "Wireless Headphones", "stock": 450},
        {"id": 102, "name": "Mechanical Keyboard", "stock": 120},
        {"id": 103, "name": "Gaming Mouse", "stock": 85},
        {"id": 104, "name": "4K Ultra HD Monitor", "stock": 40},
        {"id": 105, "name": "Orange Army Fan Jersey", "stock": 800},
        {"id": 106, "name": "Steve Smith Pro Cricket Bat", "stock": 15},
        {"id": 107, "name": "Pat Cummins Signature Cricket Ball", "stock": 250},
        {"id": 108, "name": "USB-C Hub Adapter", "stock": 310}
    ])

@app.route('/')
def home():
    return "Hello, VIT! ByteBurst is live!"

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "uptime": "100%"}), 200

@app.route('/catalog')
def get_catalog():
    products = list(collection.find({}, {"_id": 0}))
    return jsonify({"catalog": products}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)