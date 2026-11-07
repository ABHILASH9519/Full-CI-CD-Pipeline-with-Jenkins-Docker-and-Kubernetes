from app.app import app


def test_index_reports_service_status_and_version():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert response.get_json() == {
        "service": "cicd-demo",
        "status": "ok",
        "version": "0.1.0",
    }


def test_versioned_info_endpoint():
    response = app.test_client().get("/api/v1/info")
    assert response.status_code == 200
    assert response.get_json()["service"] == "cicd-demo"
    assert response.get_json()["environment"] == "local"


def test_health_endpoints():
    client = app.test_client()
    assert client.get("/health").get_json() == {"status": "alive"}
    assert client.get("/health/live").status_code == 200
    assert client.get("/health/ready").get_json() == {"status": "ready"}


def test_unknown_route_returns_consistent_json_error():
    response = app.test_client().get("/does-not-exist")
    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "not_found"


def test_security_headers_are_present_on_application_responses():
    response = app.test_client().get("/")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert response.headers["Cache-Control"] == "no-store"
    assert "frame-ancestors 'none'" in response.headers["Content-Security-Policy"]


def test_security_headers_are_also_present_on_not_found_responses():
    response = app.test_client().get("/missing")
    assert response.status_code == 404
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
