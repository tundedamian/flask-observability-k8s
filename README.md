Flask Observability on Kubernetes








Overview

This project demonstrates a Flask web application deployed on Kubernetes with a complete observability stack, including:

Prometheus: Metrics collection

Grafana: Metrics visualization

Loki + Promtail: Logging aggregation

Jaeger: Distributed tracing

OpenTelemetry: Application instrumentation

It highlights professional DevOps practices:

Dockerized application

Kubernetes manifests for deployments and services

CI/CD automation with GitHub Actions

Docker image versioning with commit SHA + branch name

Project Structure
.
├── README.md
├── flask-app
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── k8s
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── prometheus.yaml
│   ├── loki.yaml
│   ├── promtail.yaml
│   ├── jaeger.yaml
│   └── grafana.yaml
└── .github
    └── workflows
        └── ci.yml

Prerequisites

Docker >= 20.x

Kubernetes cluster (Minikube, kind, or cloud provider)

kubectl CLI installed

helm CLI (optional, for Prometheus/Grafana charts)

GitHub account with Docker Hub personal access token for CI/CD

Running Locally
docker build -t flask-observability:latest ./flask-app
docker run -it -p 5000:5000 flask-observability:latest


Access the app at: http://localhost:5000

Deploying on Kubernetes
kubectl apply -f k8s/
kubectl get pods
kubectl port-forward svc/flask-service 5000:5000


Access the app at: http://localhost:5000

Observability Stack Demo
1. Metrics with Prometheus

2. Visualizing Metrics in Grafana

3. Centralized Logs with Loki + Promtail

4. Distributed Tracing with Jaeger

5. Demo Picture of App + Metrics + Logs


CI/CD Workflow

GitHub Actions automatically builds Docker images on push

Docker images are tagged as: <DOCKERHUB_USERNAME>/<REPO_NAME>:<branch_name>-<commit_sha>

Pushes images to Docker Hub using a personal access token

Example:

tundedamian/flask-observability:main-90bd7ff
