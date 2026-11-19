# DevOps Final Project: Task Tracker

A small FastAPI and PostgreSQL task tracker demonstrating automated
testing, secure containerization, CI/CD, and local Kubernetes deployment.

## Planned architecture

- FastAPI application with two Kubernetes replicas
- PostgreSQL datastore backed by a PersistentVolumeClaim
- Kubernetes Services, ConfigMap, and Secret
- Application liveness and database-aware readiness endpoints
- GitHub Actions for linting, tests, vulnerability scanning, and GHCR publishing

## Verified development environment

- Windows with PowerShell
- Git 2.55.0.windows.3
- Python 3.13.3
- Docker Desktop 4.99.0
- Docker Engine 29.9.3 using Linux containers
- kubectl 1.36.1
- Minikube 1.39.0 using the Docker driver
- Kubernetes 1.37.0

## Cluster setup

Start Docker Desktop, then run:

```powershell
minikube start --driver=docker
kubectl wait --for=condition=Ready node/minikube --timeout=180s
kubectl get nodes
kubectl get storageclass