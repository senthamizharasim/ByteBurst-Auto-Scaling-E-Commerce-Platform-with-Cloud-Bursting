from flask import Flask, jsonify
import requests

app = Flask(__name__)

PRIMARY_URL = "http://localhost:5000"
BURST_URL = "http://localhost:5001"
MAX_PRIMARY_LATENCY = 0.40  # 400ms SLA threshold

@app.route('/api/<path:path>', methods=['GET', 'POST'])
def route_traffic(path):
    try:
        # Attempt to reach the Primary Cluster
        resp = requests.get(f"{PRIMARY_URL}/{path}", timeout=MAX_PRIMARY_LATENCY)
        return (resp.content, resp.status_code, {
            "Content-Type": "application/json",
            "X-Cluster-Routed": "Primary-Cluster"
        })
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        # Primary cluster exhausted or unreachable -> Cloud Burst triggered
        try:
            resp = requests.get(f"{BURST_URL}/{path}", timeout=2.0)
            return (resp.content, resp.status_code, {
                "Content-Type": "application/json",
                "X-Cluster-Routed": "Secondary-Burst-Cloud",
                "X-Burst-Status": "Active"
            })
        except requests.exceptions.ConnectionError:
            return jsonify({"error": "CRITICAL: Both primary and burst clusters are offline"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)