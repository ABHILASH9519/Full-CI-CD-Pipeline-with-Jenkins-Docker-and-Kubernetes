import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.app import app


def test_index_reports_service_and_status():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert response.get_json() == {"service": "cicd-demo", "status": "ok"}


def test_health_endpoint():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}
