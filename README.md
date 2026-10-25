# Full CI/CD Pipeline with Jenkins, Docker, and Kubernetes

An end-to-end portfolio project for a production-minded CI/CD workflow: code quality → security checks → tests → container build → smoke test → Kubernetes manifest validation. Deployment/publishing is intentionally gated out.

## Architecture and capabilities
- Flask API with versioned service metadata, liveness/readiness endpoints, and consistent JSON 404 errors
- Pytest suite with JUnit test reporting
- Ruff linting, Bandit static security analysis, and pip-audit dependency checks
- Jenkins declarative pipeline with quality, security, unit-test, container-build and smoke-test stages
- Non-root Docker image, image health check, slim base, and reduced runtime privileges
- Kubernetes Deployment with 2 replicas, rolling-update settings, startup/readiness/liveness probes, resource requests/limits, read-only root filesystem, dropped Linux capabilities, seccomp, and disabled service-account token mounting
- ClusterIP Service, PodDisruptionBudget and ingress NetworkPolicy
- GitHub Actions workflow validates the Python app, audits dependencies, builds and smoke-tests the image, and validates Kubernetes schemas

## Local development
Requires Python 3.12+.

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements-dev.txt
ruff check app tests
bandit -q -r app
pip-audit -r requirements.txt
pytest -q
python -m app.app
```

Local development server listens on `127.0.0.1:8080`. Routes:
- `GET /` — service status and version
- `GET /api/v1/info` — service/environment metadata
- `GET /health/live` — liveness probe
- `GET /health/ready` — readiness probe
- `GET /health` — compatibility health endpoint

## Docker
```bash
docker build -t cicd-demo:local .
docker run --rm -p 8080:8080 cicd-demo:local
```
Check `http://127.0.0.1:8080/health/ready`. The image runs Gunicorn as UID 10001, not as root.

## Jenkins
Create a Pipeline job pointing to this repository and set the script path to `Jenkinsfile`. The agent needs Git, Python 3.12, Docker Engine access, curl, and Jenkins Pipeline/JUnit plugins. Review [Jenkins setup](docs/jenkins-setup.md). Do not run untrusted pull-request code on an agent with an unrestricted Docker socket.

## Kubernetes
The manifests use `cicd-demo:local` as a local image placeholder. Build/load the image into your local cluster or change it to an immutable registry image before deploying remotely.

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/pod-disruption-budget.yaml
kubectl apply -f k8s/network-policy.yaml
kubectl rollout status deployment/cicd-demo
kubectl port-forward service/cicd-demo 8081:80
```
Then open `http://127.0.0.1:8081/health/ready`.

The NetworkPolicy restricts ingress to pods in the same namespace. If an external ingress controller or monitoring system must reach this app, explicitly allow its pod labels/namespace. NetworkPolicy enforcement depends on the cluster CNI.

## Release boundaries and limitations
- CI tests, scans, builds and smoke-tests; it does not push images or deploy to Kubernetes.
- The repository does not provision a Jenkins controller, registry, cloud account or cluster.
- Before production release, add an immutable registry tag/digest, image scanning and signing, SBOM attestation, secret management, environment-specific overlays, deployment approval, rollback automation and runtime observability.
- Pin dependencies and review pip-audit findings as upstream advisories evolve.
- Never commit credentials, kubeconfig files, registry passwords or secrets.
