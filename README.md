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
```

## Project status

## Local development

Run these commands in PowerShell from the repository's root folder.
Docker Desktop must be running with Linux containers enabled.

### First-time setup

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe setup_env.py
docker compose up -d --wait
```

The setup script generates a local .env file with a random database
password. This file is ignored by Git. PostgreSQL is available locally
on port 5433 and stores data in a named Docker volume.

### Start the application

```powershell
docker compose up -d --wait
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to create and list tasks.

- POST /tasks creates a task.
- GET /tasks retrieves saved tasks.
- GET /healthz reports application liveness.
- GET /ready checks the database connection.

### Tests and linting

With PostgreSQL running, execute these commands in another terminal:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe -m ruff check app tests setup_env.py
```

The tests use the local database and remove the task created by the
task creation/retrieval test.

### Stop local development

Stop the API with Ctrl+C in its terminal, then run:

```powershell
docker compose stop
```

This preserves the database volume and saved tasks.

## Project status

The local FastAPI/PostgreSQL application works. All 10 automated tests
and Ruff lint checks pass. Containerization of the application, CI/CD,
and Kubernetes workload deployment remain to be completed.