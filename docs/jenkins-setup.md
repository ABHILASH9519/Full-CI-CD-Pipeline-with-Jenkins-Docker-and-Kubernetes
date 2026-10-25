# Jenkins setup

## Required agent tools
- Git
- Python 3.12
- Docker Engine with permission to build/run containers
- `curl` for the smoke test
- Jenkins Pipeline and JUnit plugins

The Jenkins agent must be permitted to use Docker. Avoid giving untrusted pull-request jobs access to a privileged Docker socket; use isolated agents or a hardened build service for shared/untrusted workloads.

## Configure
1. Create a Jenkins Pipeline job pointing to this repository.
2. Ensure the agent has the tools above.
3. Set the script path to `Jenkinsfile`.
4. Run the pipeline and inspect test and container logs.

No Jenkins server or cloud cluster is provisioned by this repository.
