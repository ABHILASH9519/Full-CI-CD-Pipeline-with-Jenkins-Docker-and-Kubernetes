# Full CI/CD Pipeline with Jenkins, Docker, and Kubernetes

A practical CI/CD portfolio project demonstrating test → container build → runtime smoke test, with hardened Kubernetes manifests.

## Features
- Flask API with root and health endpoints
- Pytest unit tests and GitHub Actions CI
- Jenkins declarative pipeline with JUnit reports
- Non-root Docker image and container smoke test
- Kubernetes Deployment (2 replicas), probes, resource limits and ClusterIP Service
- Security-focused container and pod settings

## Local setup
Requires Python 3.12+.

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m app.app
```

Visit `http://127.0.0.1:8080/health`.

## Docker
```bash
docker build -t cicd-demo:local .
docker run --rm -p 8080:8080 cicd-demo:local
```
Then query `/health`. Stop the container with Ctrl+C.

## Jenkins
Create a Pipeline job pointing to this repository and set the script path to `Jenkinsfile`. The Jenkins agent needs Git, Python 3.12, Docker Engine access, curl, and the Pipeline/JUnit plugins. See [Jenkins setup](docs/jenkins-setup.md).

## Kubernetes
The manifests use `cicd-demo:local` as a local image placeholder. Build/load that image using the workflow for your local cluster, or change it to an immutable registry image for a remote cluster.

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl rollout status deployment/cicd-demo
kubectl port-forward service/cicd-demo 8081:80
```
Open `http://127.0.0.1:8081/health`.

## Pipeline scope and security
- CI tests the Python application; Jenkins builds and smoke-tests a container.
- The pipeline intentionally does not push images or deploy to Kubernetes.
- No Jenkins controller, registry, credentials, cloud account, or cluster is provisioned.
- Before production use, add image scanning, SBOM generation, signing, secret management, immutable image tags, approval gates and deployment/rollback automation.
- Never commit credentials, kubeconfig files, or Terraform/Kubernetes secrets.
