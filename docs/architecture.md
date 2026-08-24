# Architecture

## Phase 1

```text
+-------------------+       TCP 5432       +-------------------+
| FastAPI container | -------------------> | PostgreSQL        |
| Port 8000         |                      | Port 5432         |
+-------------------+                      +-------------------+
```

The application is stateless. PostgreSQL stores persistent data.

Later, the target AWS design is:

```text
Internet
   |
Route53
   |
AWS NLB
   |
NGINX Ingress
   |
FastAPI Service
   |
FastAPI Pod
   |
RDS PostgreSQL
```

ExternalDNS manages Route53 records. cert-manager obtains and renews the TLS
certificate from Let's Encrypt. GitHub Actions performs CI/security checks and
Argo CD performs GitOps-based application delivery.

## Health vs readiness

`/health` checks that the application process is running.

`/ready` checks that the application can reach PostgreSQL.

Those endpoints will later become Kubernetes liveness/readiness probes.
