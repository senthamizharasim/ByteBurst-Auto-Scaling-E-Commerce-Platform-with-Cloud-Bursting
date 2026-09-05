from flask import Flask, render_template_string, jsonify
from kubernetes import client, config
import requests

app = Flask(__name__)

# Bind directly to the active Kubernetes cluster
try:
    config.load_kube_config()
    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()
except:
    pass 

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ByteBurst Command Center</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #1a1f2b; color: #f2f2f2; display: flex; margin: 0; height: 100vh; overflow: hidden; }
        .sidebar { width: 320px; background: #141820; padding: 25px; border-right: 1px solid #2a3241; display: flex; flex-direction: column; gap: 20px; box-shadow: 2px 0 10px rgba(0,0,0,0.5); z-index: 10; }
        .main-content { flex-grow: 1; display: flex; flex-direction: column; background: #1a1f2b; }
        .tabs { display: flex; background: #141820; border-bottom: 2px solid #2a3241; }
        .tab { padding: 15px 25px; cursor: pointer; color: #8892b0; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; font-size: 13px; transition: color 0.2s; }
        .tab.active { color: #e6a94d; border-bottom: 3px solid #e6a94d; background: #1a1f2b; }
        .tab:hover { color: #e6a94d; }
        iframe { flex-grow: 1; border: none; width: 100%; height: 100%; display: none; }
        iframe.active { display: block; }
        .card { background: #232936; padding: 20px; border-radius: 12px; border: 1px solid #2a3241; }
        h2 { margin-top: 0; color: #e6a94d; font-size: 20px; letter-spacing: 0.5px; }
        h3 { margin-top: 0; font-size: 14px; color: #8892b0; text-transform: uppercase; letter-spacing: 1px; }
        button { width: 100%; padding: 12px; margin-top: 15px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; transition: all 0.2s; font-size: 14px; }
        .btn-green { background: #4c9f70; color: white; }
        .btn-green:hover { background: #3d825b; box-shadow: 0 0 10px rgba(76,159,112,0.4); }
        .btn-red { background: #d9534f; color: white; }
        .btn-red:hover { background: #c9302c; box-shadow: 0 0 10px rgba(217,83,79,0.4); }
        .status { font-size: 28px; font-weight: bold; color: #4c9f70; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>ByteBurst Command Center</h2>
        
        <div class="card">
            <h3>Active Primary Pods</h3>
            <div class="status" id="pod-count">Loading...</div>
        </div>

        <div class="card">
            <h3>Routing Status</h3>
            <div class="status" id="route-status" style="color: #4c9f70;">Primary Zone</div>
        </div>

        <div class="card">
            <h3>Execution Triggers</h3>
            <button class="btn-green" onclick="startLocust()">Start Locust Swarm</button>
            <button class="btn-red" onclick="triggerBurst()">Kill Primary Cluster (Failover)</button>
            <button class="btn-green" style="background: #e6a94d; color: #141820;" onclick="resetCluster()">Restore Primary Architecture</button>
        </div>
    </div>
    
    <div class="main-content">
        <div class="tabs">
            <div class="tab active" onclick="switchTab('storefront', this)">Storefront</div>
            <div class="tab" onclick="switchTab('telemetry', this)">Grafana Telemetry</div>
            <div class="tab" onclick="switchTab('stress', this)">Locust Load Test</div>
        </div>
        
        <!-- Localhost ports used temporarily; NGINX Ingress will handle this in the cloud -->
        <iframe id="storefront" class="active" src="http://localhost:3000"></iframe>
        <iframe id="telemetry" src="http://localhost:3000/d/metrics"></iframe> 
        <iframe id="stress" src="http://localhost:8089"></iframe>
    </div>

    <script>
        function switchTab(tabId, element) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('iframe').forEach(i => i.classList.remove('active'));
            element.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }

        function updateMetrics() {
            fetch('/api/metrics').then(r => r.json()).then(data => {
                document.getElementById('pod-count').innerText = data.pods;
                let routeEl = document.getElementById('route-status');
                
                // Real-time failover detection based on live pod count
                if(data.pods.startsWith("0")) {
                    routeEl.innerText = "Burst Cloud Active";
                    routeEl.style.color = "#d9534f";
                } else {
                    routeEl.innerText = "Primary Zone";
                    routeEl.style.color = "#4c9f70";
                }
            });
        }
        setInterval(updateMetrics, 2000);

        function triggerBurst() {
            fetch('/api/failover', {method: 'POST'});
            alert('CRITICAL: Primary deployment scaling to 0. Real traffic is now rerouting to the burst-cloud namespace.');
        }

        function resetCluster() {
            fetch('/api/reset', {method: 'POST'});
            alert('Architecture restored. Primary deployment scaling back to minimum limits.');
        }

        function startLocust() {
            alert('Switching to the Locust panel. Configure your users and spawn rate to hammer the cluster!');
            switchTab('stress', document.querySelectorAll('.tab')[2]);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/metrics')
def metrics():
    try:
        pods = v1.list_namespaced_pod(namespace="default", label_selector="app=byteburst-backend")
        running = sum(1 for pod in pods.items if pod.status.phase == "Running")
        return jsonify({"pods": f"{running} / 5 Replicas"})
    except Exception as e:
        return jsonify({"pods": "API Disconnected"})

@app.route('/api/failover', methods=['POST'])
def failover():
    try:
        # Executes a real Kubernetes command to scale the primary deployment to 0
        scale = {"spec": {"replicas": 0}}
        apps_v1.patch_namespaced_deployment_scale(name="byteburst-backend-deployment", namespace="default", body=scale)
        return jsonify({"status": "failed_over"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/reset', methods=['POST'])
def reset():
    try:
        # Executes a real Kubernetes command to restore the deployment
        scale = {"spec": {"replicas": 2}}
        apps_v1.patch_namespaced_deployment_scale(name="byteburst-backend-deployment", namespace="default", body=scale)
        return jsonify({"status": "reset"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)