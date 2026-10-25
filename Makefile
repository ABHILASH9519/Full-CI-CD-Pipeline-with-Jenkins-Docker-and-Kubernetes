PYTHON ?= python3
IMAGE ?= cicd-demo:local
PORT ?= 8080

.PHONY: install lint security test check docker-build docker-smoke clean

install:
	$(PYTHON) -m pip install -r requirements-dev.txt

lint:
	ruff check app tests

security:
	bandit -q -r app
	pip-audit -r requirements.txt

test:
	pytest -q --junitxml=test-results.xml

check: lint security test

docker-build:
	docker build --tag $(IMAGE) .

docker-smoke: docker-build
	@set -eu; \
	  docker run --detach --rm --name cicd-demo-make -p $(PORT):8080 $(IMAGE); \
	  cleanup() { docker stop cicd-demo-make >/dev/null 2>&1 || true; }; \
	  trap cleanup EXIT; \
	  for attempt in $$(seq 1 30); do \
	    if curl --fail --silent http://127.0.0.1:$(PORT)/health/ready; then \
	      curl --fail --silent http://127.0.0.1:$(PORT)/api/v1/info; exit 0; \
	    fi; sleep 1; \
	  done; \
	  docker logs cicd-demo-make; exit 1

clean:
	rm -rf .pytest_cache .ruff_cache __pycache__ app/__pycache__ tests/__pycache__ test-results.xml
