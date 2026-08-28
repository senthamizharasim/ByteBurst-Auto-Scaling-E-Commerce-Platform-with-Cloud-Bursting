<img width="932" height="447" alt="Screenshot 2026-08-28 135502" src="https://github.com/user-attachments/assets/dd98caa9-28f3-4488-8f3b-aed5bc0ce7c1" />
<img width="754" height="404" alt="Screenshot 2026-08-28 135535" src="https://github.com/user-attachments/assets/a250cff6-8fff-48b5-82ef-27d89933290b" />
<img width="878" height="302" alt="Screenshot 2026-08-28 152734" src="https://github.com/user-attachments/assets/38809e40-595f-4469-b209-650b35ca715e" />
<img width="747" height="384" alt="Screenshot 2026-08-28 153345" src="https://github.com/user-attachments/assets/27cf073d-c88d-405e-81af-29d8825704d2" />
<img width="746" height="430" alt="Screenshot 2026-08-28 153548" src="https://github.com/user-attachments/assets/44c54e3f-0826-4ddf-b05e-847548391dc8" />
# ByteBurst: Auto-Scaling E-Commerce Platform with Cloud Bursting

Modern retail applications experience highly unpredictable traffic patterns, especially during flash sales. This project implements a containerized e-commerce backend deployed on a Kubernetes cluster with integrated monitoring, load-balancing, and automated scaling to handle dynamic traffic spikes efficiently.

## 🛠️ Tech Stack
* **Application Framework:** Python / Flask
* **Containerization:** Docker
* **Container Orchestration:** Kubernetes (Minikube)
* **Load Balancing:** Kubernetes NodePort Service
* **Monitoring:** Kubernetes Metrics Server & Minikube Dashboard

## 🚀 Current Progress (Review 2: 50% Implementation)
- [x] Abstract and architectural flow diagram completed.
- [x] Developed lightweight Python/Flask backend microservice.
- [x] Containerized application using Docker.
- [x] Deployed Pods and Services via Kubernetes manifests (`deployment.yaml`).
- [x] Established basic load balancing across replicated pods.
- [x] Configured Minikube metrics-server and enabled visual monitoring dashboard.

## 💻 Local Setup & Run Instructions

**1. Start the local cluster:**
```bash
minikube start
```

**2. Build the Docker image and load it into Minikube:**
```bash
docker build -t byteburst-backend .
minikube image load byteburst-backend
```

**3. Deploy the application to Kubernetes:**
```bash
kubectl apply -f deployment.yaml
```

**4. Open the secure tunnel to access the app:**
```bash
kubectl port-forward service/byteburst-backend-service 5000:5000
```
*The app will now be live at `http://localhost:5000`*

**5. View the monitoring dashboard:**
```bash
minikube addons enable metrics-server
kubectl proxy --address='0.0.0.0' --port=8001 --accept-hosts='^.*'
```
*Access the dashboard via Chrome at `http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/`*

## 🔮 Future Scope (Review 3 Phase)
* Implementation of Horizontal Pod Autoscaler (HPA) to react to CPU thresholds.
* Simulation of heavy traffic spikes using Locust.
* Integration of a cloud-bursting failover handler for overflow traffic routing.
