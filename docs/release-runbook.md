# Release and rollback runbook

## Current release boundary
The automated workflows test source, run static checks, build the container, smoke-test it and validate Kubernetes schemas. They do **not** publish images or apply manifests to a cluster. Any deployment described below is an operator-run procedure, not an existing integration.

## Pre-release checklist
- [ ] Review CI results for the exact commit to be released.
- [ ] Review Ruff, Bandit and pip-audit findings; resolve or document accepted risk.
- [ ] Build an image from the reviewed commit and tag it with an immutable commit SHA.
- [ ] Scan the image and generate an SBOM; archive both reports with the release.
- [ ] Push to an approved registry using a short-lived credential outside source control.
- [ ] Update the deployment image to the immutable registry digest and validate manifests.
- [ ] Confirm namespace, NetworkPolicy reachability, resource quotas, monitoring and rollback target.
- [ ] Obtain environment-owner approval before applying production changes.

## Rollout
1. Review the complete diff and rendered manifests.
2. Apply manifests in a non-production namespace first.
3. Watch `kubectl rollout status deployment/cicd-demo` and inspect pod events/logs.
4. Test `/health/ready` and `/api/v1/info` through the service.
5. Confirm both replicas become ready and the previous ReplicaSet remains available.

## Rollback
- Use `kubectl rollout history deployment/cicd-demo` to inspect revisions.
- Roll back with `kubectl rollout undo deployment/cicd-demo` only after confirming the target revision.
- Re-check rollout status, readiness and service behavior.
- Capture events/logs and record the failed image digest and change.
- If a schema or configuration change is incompatible, restore the corresponding compatible configuration as well.

## Incident notes
Never paste credentials, tokens, kubeconfig contents or sensitive customer data into CI logs or issue reports. The example app is stateless and has no database migration path; real services must document data rollback separately.
