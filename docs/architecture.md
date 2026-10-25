# System Architecture

This page provides full-size, version-controlled SVG diagrams also embedded in the repository README. SVG assets are used so the diagrams display in Markdown viewers that do not render Mermaid code blocks.

## Component architecture

![CI/CD system architecture](images/system-architecture.svg)

## CI workflow

![CI/CD validation flow](images/cicd-flow.svg)

## Kubernetes request path

![Kubernetes topology](images/kubernetes-topology.svg)

## Component responsibilities

| Component | Responsibility |
|---|---|
| GitHub Actions | Repeatable lint, static security, dependency audit, tests, Docker smoke test, Kubernetes schema validation |
| Jenkinsfile | Jenkins-agent pipeline for quality/security checks, unit tests, image build and smoke test |
| Dockerfile | Reproducible runtime image using a non-root account and health check |
| Kubernetes Deployment | Two replicas, probes, rolling update, resource bounds and pod security settings |
| Service | Stable internal endpoint for application pods |
| PodDisruptionBudget | Protects a minimum of one available pod during supported voluntary disruptions |
| NetworkPolicy | Restricts ingress to same-namespace pods; requires compatible CNI enforcement |

## Deployment boundary

The CI workflow does not publish images or apply Kubernetes manifests. The manifests are examples and use `cicd-demo:local`; a remote deployment requires a registry image pinned by immutable digest, cluster-specific network rules, secrets managed outside Git, and an approved release process.
