pipeline {
  agent any
  options { timestamps(); disableConcurrentBuilds() }
  environment {
    IMAGE_NAME = 'cicd-demo'
    IMAGE_TAG = "${BUILD_NUMBER}"
  }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Install dependencies') {
      steps {
        sh 'python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements-dev.txt'
      }
    }
    stage('Quality and security') {
      steps {
        sh '''
          . .venv/bin/activate
          ruff check app tests
          bandit -q -r app
          pip-audit -r requirements.txt
        '''
      }
    }
    stage('Unit tests') {
      steps {
        sh '. .venv/bin/activate && pytest -q --junitxml=test-results.xml'
      }
    }
    stage('Build container') {
      steps {
        sh 'docker build --tag ${IMAGE_NAME}:${IMAGE_TAG} .'
      }
    }
    stage('Container smoke test') {
      steps {
        sh '''
          set -eu
          docker run --detach --rm --name cicd-demo-test -p 18080:8080 ${IMAGE_NAME}:${IMAGE_TAG}
          cleanup() { docker stop cicd-demo-test >/dev/null 2>&1 || true; }
          trap cleanup EXIT
          for attempt in $(seq 1 30); do
            if curl --fail --silent http://127.0.0.1:18080/health/ready; then
              curl --fail --silent http://127.0.0.1:18080/api/v1/info
              exit 0
            fi
            sleep 1
          done
          docker logs cicd-demo-test
          exit 1
        '''
      }
    }
  }
  post {
    always {
      junit allowEmptyResults: true, testResults: 'test-results.xml'
      sh 'docker image rm ${IMAGE_NAME}:${IMAGE_TAG} >/dev/null 2>&1 || true'
      cleanWs()
    }
  }
}
