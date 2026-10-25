# CI/CD threat model

## Assets
Source code, dependency integrity, container images, Jenkins agent credentials, registry credentials, Kubernetes API access, and release integrity.

## Trust boundaries
- GitHub pull requests and branch content are untrusted until reviewed.
- Jenkins agents execute repository-controlled scripts and therefore must be isolated from privileged credentials.
- Docker daemon access can grant host-level control; do not expose it to untrusted PR builds.
- Kubernetes manifests are declarative input and require review before cluster application.
- Registry and cluster credentials must be injected through protected secret stores, never committed to Git.

## Main risks and current controls
| Risk | Current control | Remaining work |
|---|---|---|
| Vulnerable Python dependency | `pip-audit` in CI | Review/patch advisories continuously |
| Unsafe Python patterns | Bandit static analysis | Add application-specific threat review |
| Inconsistent style/regressions | Ruff and pytest | Expand coverage as features grow |
| Container runs as root | UID 10001 in Dockerfile | Add image signing and runtime policy |
| Privilege escalation in pod | Drop all capabilities, non-root, seccomp, read-only root FS | Enforce policy at cluster admission |
| Accidental disruption | Two replicas, rolling update, PDB | Validate cluster capacity and topology |
| Unrestricted pod ingress | Namespace-scoped NetworkPolicy | Configure approved ingress/monitoring sources |
| Unreviewed production rollout | No automated deployment in CI | Add protected environment approvals before deployment |

## Explicit non-goals
This repository does not yet provide a registry integration, secrets backend, image signing, deployment credentials, cluster provisioning, or production monitoring. The security controls reduce risk but do not constitute a production certification.
