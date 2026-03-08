from flask import Flask, jsonify, request
from collections import defaultdict
import redis
import logging
import os
import time
import json

app = Flask(__name__)

request_counts = defaultdict(int)

@app.before_request
def log_request():
    request.start_time = time.time()
    request_counts[request.path] += 1

    if request.path == "/health":
        logger.debug(f"Incoming request: {request.method} {request.path}")
    else:
        logger.info(f"Incoming request: {request.method} {request.path}")

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("Flask application starting up")

# Redis initialization
redis_client = None

def init_redis():
    """Initialize Redis client from REDIS_HOST/REDIS_PORT (+ optional REDIS_PASSWORD)."""
    global redis_client

    host = os.getenv("REDIS_HOST")
    port = int(os.getenv("REDIS_PORT", "6379"))
    password = os.getenv("REDIS_PASSWORD")  # optional

    if not host:
        logger.warning("REDIS_HOST not set. Redis will not be initialized.")
        redis_client = None
        return

    try:
        logger.info(f"Initializing Redis client host={host} port={port} tls=True password={'set' if password else 'not set'}")

        redis_client = redis.Redis(
            host=host,
            port=port,
            password=password,
            decode_responses=True,
            ssl=True,
            socket_connect_timeout=5,
            socket_timeout=5,
        )

        redis_client.ping()
        logger.info("Connected to Redis successfully")

    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
        redis_client = None

# Initialize Redis when app starts
init_redis()

# Routes
@app.route("/")
def home():
    return "Hello from Flask + Redis with Docker Compose!"

@app.route("/health")
def health():
    logger.info("/health endpoint accessed")

    if redis_client is None:
        return jsonify({"status": "DEGRADED", "redis": "not connected"}), 200

    try:
        redis_client.ping()
        return jsonify({"status": "OK", "redis": "connected"}), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"status": "DEGRADED", "redis": "unreachable"}), 200

@app.route("/count")
def count():
    global redis_client

    if redis_client is None:
        init_redis()

    if redis_client is None:
        logger.error("Redis not initialized in /count")
        return jsonify({"error": "Redis not initialized"}), 500

    try:
        visits = redis_client.incr("counter")
        logger.info(f"/count called. Visits={visits}")
        return jsonify({"visits": visits}), 200
    except Exception as e:
        logger.error(f"Error in /count endpoint: {e}")
        return jsonify({"error": "Redis error"}), 500

@app.route("/metrics")
def metrics():
    return jsonify({
        "requests_total": sum(request_counts.values()),
        "requests_by_path": dict(request_counts)
    }), 200

@app.after_request
def log_response(response):
    duration = time.time() - request.start_time
    logger.info(
        json.dumps({
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration_ms": round(duration *1000, 2),
            "ip": request.remote_addr
        })
    )
    return response

# App entry point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


