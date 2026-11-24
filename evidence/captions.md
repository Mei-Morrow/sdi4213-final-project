# Milestone Evidence
## 01 - Local application works

File: 01-local-app.png

The local FastAPI application retrieves the previously created task
"Verify local PostgreSQL storage" through GET /tasks. The HTTP 200
response and saved record demonstrate successful reading of data
written to PostgreSQL.

## 02 - Automated tests pass

File: 02-tests-pass.png

All 10 automated tests pass using pytest. The tests verify application
information, liveness, database-aware readiness, rejection of invalid
task titles, task creation and retrieval through PostgreSQL, and safe
HTTP 503 responses during a simulated database outage.

## 09 - Cluster ready

File: 09-cluster-ready.png

Minikube v1.39.0 is installed, and kubectl shows the local Minikube node
in Ready status running Kubernetes v1.37.0.