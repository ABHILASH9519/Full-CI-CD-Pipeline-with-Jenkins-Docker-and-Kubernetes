# System Architecture

This page is the source companion for the diagrams embedded in the repository README. GitHub renders the Mermaid diagrams directly, so they stay version-controlled with the documentation.

## Component architecture

```mermaid
flowchart LR
    Dev[Developer] --> Repo[GitHub Repository]
    Repo --> GHA[GitHub Actions]
    Repo --> Jenkins[Jenkins Pipeline]
    GHA --> Quality[Lint + Security + Tests]
    Jenkins --> Quality
    Quality --> Image[Docker Image]
    Image --> Smoke[Container Smoke Test]
    Smoke --> Manifests[Kubernetes YAML]
    Manifests --> Deployment[Deployment · 2 replicas]
    Deployment --> Service[ClusterIP Service]
    Service --> API[Flask + Gunicorn]
    PDB[PodDisruptionBudget] -. availability .-> Deployment
    NetworkPolicy[NetworkPolicy] -. ingress restriction .-> API
```

## CI workflow

```mermaid
flowchart TD
    Start([Push / Pull Request]) --> Checkout[Checkout]
    Checkout --> Install[Install dependencies]
    Install --> Ruff[Ruff]
    Ruff --> Bandit[Bandit]
    Bandit --> Audit[pip-audit]
    Audit --> Tests[pytest + JUnit]
    Tests --> Build[Docker build]
    Build --> Run[Run container]
    Run --> Health{Readiness passes?}
    Health -- No --> Fail[Fail and capture logs]
    Health -- Yes --> Schema[Kubernetes schema validation]
    Schema --> End([CI checks complete])
```

## Kubernetes request path

```mermaid
flowchart TB
    Client[Allowed in-namespace client] --> Service[ClusterIP Service :80]
    Service --> PodA[Pod A :8080]
    Service --> PodB[Pod B :8080]
    Policy[Ingress NetworkPolicy] -. restricts .-> PodA
    Policy -. restricts .-> PodB
    PDB[PodDisruptionBudget minAvailable 1] -. protects availability .-> PodA
    PDB -. protects availability .-> PodB
```

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
