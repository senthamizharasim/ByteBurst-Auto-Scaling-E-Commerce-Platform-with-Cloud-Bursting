from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, VIT! ByteBurst is live!"

# The self-healing endpoint
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "uptime": "100%"}), 200

# The simulated e-commerce database
@app.route('/catalog')
def get_catalog():
    products = [
        {"id": 101, "name": "Wireless Headphones", "stock": 450},
        {"id": 102, "name": "Mechanical Keyboard", "stock": 120},
        {"id": 103, "name": "Gaming Mouse", "stock": 85}
    ]
    return jsonify({"catalog": products}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)