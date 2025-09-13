# Flask Observability on Kubernetes

This repository contains a **Flask application** deployed on a **Kubernetes cluster** with a full observability stack using **Prometheus, Grafana, Loki, Jaeger, and Promtail**.

---

## Project Architecture

- **Flask App**: Python web application with `/metrics` endpoint for Prometheus scraping and `/error` endpoint for simulating errors.
- **Prometheus**: Scrapes metrics from Flask app and other targets.
- **Grafana**: Visualizes metrics collected by Prometheus.
- **Loki**: Centralized log aggregation.
- **Promtail**: DaemonSet that tails logs from containers and sends them to Loki.
- **Jaeger**: Distributed tracing for the Flask app.

### Kubernetes Architecture

Namespace: default
├─ Deployment: flask-app
├─ Deployment: grafana
├─ Deployment: prometheus
├─ Deployment: jaeger
├─ Deployment: loki
├─ DaemonSet: promtail
└─ Services: NodePort for Flask, Grafana, Prometheus, Jaeger

yaml
Copy code

---

## Prerequisites

- Docker
- Kubernetes cluster (Minikube recommended)
- `kubectl` configured to your cluster
- Git

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/tundedamian/flask-observability-k8s.git
cd flask-observability-k8s
```

Start Minikube (if using Minikube)

```bash
minikube start
```

Build and push Docker image

```bash
docker build -t tundedamian/flask-observability:latest .
docker push tundedamian/flask-observability:latest
Apply Kubernetes manifests
```

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/promtail-rbac.yaml
kubectl apply -f k8s/promtail-config.yaml
kubectl apply -f k8s/promtail.yaml
kubectl apply -f k8s/prometheus.yaml
kubectl apply -f k8s/grafana.yaml
kubectl apply -f k8s/loki.yaml
kubectl apply -f k8s/jaeger.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Check all pods are running

```bash
kubectl get pods -o wide
```

Access services via Minikube

```bash
minikube service flask-service
minikube service grafana
minikube service prometheus
minikube service jaeger
```

Observability Features
Metrics: Flask app exposes Prometheus metrics.

Logging: Promtail collects container logs, Loki stores them, and Grafana visualizes them.

Tracing: Jaeger captures traces for Flask app requests.

Logs Monitoring with Promtail
Promtail runs as a DaemonSet and collects logs from /var/log/containers and /var/lib/docker/containers.

Ensure Promtail has the proper service account and RBAC permissions.

Notes
DaemonSet promtail has both name and app labels for easy selection:

```bash
kubectl get pods -n default -l name=promtail
kubectl get pods -n default -l app=promtail
```

Use /error endpoint in Flask to test tracing with Jaeger.

Author
Ogedengbe Damian Olatunde
GitHub: tundedamian
LinkedIn: linkedin.com/in/teedam
