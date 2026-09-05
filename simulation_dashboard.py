from flask import Flask, render_template_string, jsonify
import subprocess
import requests
import threading
import time

app = Flask(__name__)

PRIMARY_URL = "http://localhost:5000"
BURST_URL = "http://localhost:5001"
load_active = False

def generate_load():
    global load_active
    load_active = True
    timeout = time.time() + 60
    while time.time() < timeout and load_active:
        try:
            requests.get(f"{PRIMARY_URL}/api/products", timeout=0.5)
        except:
            pass
    load_active = False

@app.route('/')
def dashboard():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ByteBurst Command Center</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #121212; color: #fff; display: flex; margin: 0; height: 100vh; }
            .sidebar { width: 350px; background: #1e1e1e; padding: 20px; border-right: 2px solid #333; }
            .storefront { flex-grow: 1; border: none; }
            .card { background: #2a2a2a; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
            button { width: 100%; padding: 10px; margin-top: 10px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
            .btn-orange { background: #ff6600; color: white; }
            .btn-red { background: #cc0000; color: white; }
            .status { font-size: 24px; font-weight: bold; color: #00ff00; }
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h2>ByteBurst Infrastructure</h2>
            
            <div class="card">
                <h3>Active Backend Pods (Primary)</h3>
                <div class="status" id="pod-count">Loading...</div>
            </div>

            <div class="card">
                <h3>Traffic Routing</h3>
                <div class="status" id="route-status">Primary Cluster</div>
            </div>

            <div class="card">
                <h3>Simulation Controls</h3>
                <button class="btn-orange" onclick="startLoad()">Simulate Flash Sale (Trigger HPA)</button>
                <button class="btn-red" onclick="triggerBurst()">Simulate Primary Failure (Cloud Burst)</button>
            </div>
        </div>
        
        <iframe class="storefront" src="http://localhost:3000"></iframe>

        <script>
            function updateMetrics() {
                fetch('/metrics').then(r => r.json()).then(data => {
                    document.getElementById('pod-count').innerText = data.pods + ' / 5 Replicas';
                    document.getElementById('route-status').innerText = data.route;
                    document.getElementById('route-status').style.color = data.route.includes('Burst') ? '#ffcc00' : '#00ff00';
                });
            }
            setInterval(updateMetrics, 2000);

            function startLoad() {
                fetch('/start-load');
                alert('Flash sale traffic initiated! Watch the pod count scale up over the next 30 seconds.');
            }

            function triggerBurst() {
                fetch('/trigger-burst');
                alert('Primary cluster connection killed. Traffic is now bursting to the secondary namespace.');
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/metrics')
def metrics():
    try:
        output = subprocess.check_output(["kubectl", "get", "pods", "-n", "default", "-l", "app=byteburst-backend"], text=True)
        pod_count = output.count("Running")
    except:
        pod_count = 0
        
    try:
        resp = requests.get(f"{PRIMARY_URL}/api/products", timeout=0.5)
        route = "Primary Cluster"
    except:
        route = "Secondary Burst Cloud Active"
        
    return jsonify({"pods": pod_count, "route": route})

@app.route('/start-load')
def start_load():
    threading.Thread(target=generate_load).start()
    return {"status": "loading"}

@app.route('/trigger-burst')
def trigger_burst():
    subprocess.Popen(["kubectl", "delete", "service", "byteburst-backend-service", "-n", "default"])
    return {"status": "bursting"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)