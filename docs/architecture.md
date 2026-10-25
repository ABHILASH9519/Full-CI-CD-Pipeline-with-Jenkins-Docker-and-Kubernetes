# Pipeline architecture

1. Jenkins checks out the repository.
2. A Python virtual environment is created and unit tests run.
3. Docker builds a non-root application image.
4. A smoke test starts the image and checks `/health`.
5. Kubernetes manifests define a two-replica Deployment and internal ClusterIP Service.

The pipeline deliberately stops before publishing an image or deploying to a cluster. A real release needs a configured registry, credentials stored in Jenkins Credentials, image scanning/signing, and an approved target cluster. Never place registry passwords or kubeconfig contents in the repository.
