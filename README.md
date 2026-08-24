# CoderCo Assignment 2 — Cloud Change Tracker

This is Phase 1 of the CoderCo Assignment 2 project. It is a small DevOps-style
application for recording cloud/deployment changes.

The final project will grow in controlled phases:

1. Application + PostgreSQL
2. Docker + Compose
3. Terraform AWS infrastructure
4. Kubernetes
5. NGINX Ingress + ExternalDNS + Route53 + cert-manager + Let's Encrypt
6. GitHub Actions + Trivy + Checkov + pre-commit + Makefile
7. Argo CD GitOps
8. Prometheus + Grafana

## Phase 1 architecture

```text
Browser / API client
        |
        v
   FastAPI app
        |
        | PostgreSQL TCP/5432
        v
 PostgreSQL database
```

The app is intentionally modest: one API and one database. The database gives us
real persistence so the later Kubernetes/AWS architecture has a meaningful use case.

## API

- `GET /health` — process health
- `GET /ready` — application + database readiness
- `GET /changes` — list changes
- `GET /changes/{id}` — retrieve one change
- `POST /changes` — create a change
- `PUT /changes/{id}` — update a change
- `DELETE /changes/{id}` — delete a change
- `GET /docs` — FastAPI interactive API documentation

## Run locally

```bash
cp .env.example .env
docker compose up --build
```

Open:

```text
http://localhost:8000/docs
```

Test:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/ready
```

Run tests:

```bash
pip install -r requirements.txt
pytest
```

## Final assignment architecture

```text
Internet
   |
Route53
   |
AWS Network Load Balancer
   |
NGINX Ingress
   |
FastAPI Service
   |
FastAPI Pod
   |
RDS PostgreSQL

ExternalDNS ---> Route53
cert-manager ---> Let's Encrypt ---> TLS Secret
GitHub Actions ---> Registry ---> GitOps ---> Argo CD ---> EKS
Prometheus ---> Grafana
```

## CoderCo requirement mapping

| Requirement | Planned location |
|---|---|
| Terraform IaC | `terraform/` — Phase 3 |
| Terraform modules | `terraform/modules/` — Phase 3 |
| EKS | `terraform/` — Phase 3 |
| NGINX Ingress | `helm/` + `k8s/` — Phase 5 |
| cert-manager | `helm/` + `k8s/` — Phase 5 |
| Let's Encrypt | cert-manager ClusterIssuer — Phase 5 |
| ExternalDNS | `helm/` + IAM/Route53 — Phase 5 |
| Custom domain | Route53 + Ingress — Phase 5 |
| HTTPS enforced | NGINX redirect + TLS — Phase 5 |
| Trivy | `.github/workflows/` — Phase 6 |
| Checkov | `.github/workflows/` + pre-commit — Phase 6 |
| GitHub Actions | `.github/workflows/` — Phase 6 |
| pre-commit | `.pre-commit-config.yaml` — Phase 6 |
| Makefile | root `Makefile` — Phase 6 |
| Argo CD | `argocd/` — Phase 7 |
| Prometheus/Grafana | `helm/` — Phase 8 |
| Architecture diagram | `docs/architecture.md` |
| Detailed teaching docs | `docs/` |

The assignment requirements are not being removed. We are implementing them in
layers so each component can be understood and tested before the next one is added.

## Scope

For this small project we will not add replicas everywhere just to make numbers
look production-grade. The initial application target is one FastAPI replica.
High availability will be demonstrated only where it provides meaningful value,
and the final database will be Amazon RDS rather than a PostgreSQL cluster inside
Kubernetes.
