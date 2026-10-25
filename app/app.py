import os

from flask import Flask, jsonify

app = Flask(__name__)
SERVICE_NAME = "cicd-demo"
SERVICE_VERSION = os.getenv("APP_VERSION", "0.1.0")


@app.get("/")
def index():
    return jsonify(service=SERVICE_NAME, status="ok", version=SERVICE_VERSION)


@app.get("/api/v1/info")
def info():
    return jsonify(
        service=SERVICE_NAME,
        version=SERVICE_VERSION,
        environment=os.getenv("APP_ENV", "local"),
    )


@app.get("/health")
@app.get("/health/live")
def liveness():
    return jsonify(status="alive"), 200


@app.get("/health/ready")
def readiness():
    # Add dependency checks here if the service later depends on a database or queue.
    return jsonify(status="ready"), 200


@app.errorhandler(404)
def not_found(_error):
    return jsonify(error={"code": "not_found", "message": "Resource not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
