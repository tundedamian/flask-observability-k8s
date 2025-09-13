# Flask Observability on Kubernetes

This project demonstrates deploying a Flask application with observability stack on Kubernetes using **Prometheus**, **Grafana**, **Jaeger**, **Loki**, and **Promtail**. It showcases metrics, logging, and tracing for a microservices-style Flask app.

---

## Prerequisites

- Kubernetes cluster (Minikube recommended)
- `kubectl` installed
- Docker installed and configured
- Basic knowledge of Kubernetes resources (Deployment, Service, DaemonSet, ConfigMap)

---

## Deployment

All Kubernetes manifests are stored in the `k8s/` directory.  

### Steps:

1. Create the namespace:
   
```bash
kubectl apply -f k8s/namespace.yaml
```

2. Deploy Prometheus:

```bash
kubectl apply -f k8s/prometheus.yaml
```

3. Deploy Grafana:

```bash
kubectl apply -f k8s/grafana.yaml
```

4. Deploy Jaeger:

```bash
kubectl apply -f k8s/jaeger.yaml
```

5. Deploy Loki:

```bash
kubectl apply -f k8s/loki.yaml
```
6. Deploy Promtail (with RBAC):

```bash
kubectl apply -f k8s/promtail-rbac.yaml
kubectl apply -f k8s/promtail-config.yaml
kubectl apply -f k8s/promtail.yaml
```

7. Deploy the Flask app:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

8. Verifying Deployments
Check Promtail pods
Promtail pods can be selected using either the name or app label:

```bash
kubectl get pods -n default -l name=promtail
kubectl get pods -n default -l app=promtail
```

9. Check Flask app pods
```bash
kubectl get pods -n default -l app=flask-app
```

10. Testing Observability

Metrics: Visit the Flask app /metrics endpoint to verify Prometheus metrics are exposed.

Tracing: Trigger the /error endpoint in Flask to test tracing with Jaeger.

Logging: Verify logs are collected by Promtail and available in Grafana Loki.

11. Access Services via Minikube
Retrieve the Minikube IP:

```bash
minikube ip
```

12. Access services via NodePort:

Flask: http://<minikube-ip>:31152

Grafana: http://<minikube-ip>:30190

Prometheus: http://<minikube-ip>:32434

Jaeger: http://<minikube-ip>:31735

Project Structure
```csharp
flask-observability-k8s/
├─ flask-app/               # Flask application code
├─ k8s/                     # Kubernetes manifests
│  ├─ deployment.yaml
│  ├─ service.yaml
│  ├─ grafana.yaml
│  ├─ prometheus.yaml
│  ├─ jaeger.yaml
│  ├─ loki.yaml
│  ├─ promtail.yaml
│  ├─ promtail-config.yaml
│  ├─ promtail-rbac.yaml
│  └─ namespace.yaml
└─ README.md
```

Author
Ogedengbe Damian Olatunde
GitHub: tundedamian
LinkedIn: linkedin.com/in/teedam
