# CoderCo Assignment 2 Requirement Plan

The original assignment requirements remain part of this project. We are implementing
them in phases rather than adding everything before the application works.

## Required infrastructure

- Terraform VPC
- Terraform EKS
- reusable Terraform modules
- security groups
- small managed node group
- RDS PostgreSQL

Location: `terraform/` in the next phases.

## Required Kubernetes/Helm

- NGINX Ingress Controller
- cert-manager
- Let's Encrypt
- ExternalDNS
- custom `app.<your-domain>` hostname
- HTTPS enforced

Locations: `helm/` and `k8s/`.

## Required security

- Trivy container/filesystem scanning in GitHub Actions
- Checkov Terraform scanning in GitHub Actions
- Checkov/security validation through pre-commit
- `.env` ignored and secrets never committed

Locations: `.github/workflows/` and `.pre-commit-config.yaml`.

## Required CI/CD

GitHub Actions will eventually:

1. test the application
2. run Checkov
3. run Trivy
4. build the container
5. scan the image
6. publish the image
7. update the GitOps desired state

## Required automation

A root `Makefile` will expose commands such as:

```text
make test
make build
make scan
make tf-fmt
make tf-validate
make tf-plan
make tf-apply
make tf-destroy
```

## Optional Argo CD

Argo CD will reconcile Kubernetes manifests from Git.

## Bonus monitoring

A deliberately small monitoring stack will be added later:

- Prometheus
- Grafana
- a few meaningful alerts

## Small-project replica strategy

We will not create replicas everywhere simply to make the project look larger.

Initial application target: **1 FastAPI replica**.

Where availability matters, we can use a small number of replicas later. The final
database will be RDS rather than a PostgreSQL cluster inside Kubernetes.

This reduces cost and complexity while preserving the assignment's required concepts.
