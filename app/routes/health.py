from flask import Blueprint, jsonify
from app.database import get_db
from app.utils.logger import get_logger
from app.middleware.rate_limiter import limiter

health_bp = Blueprint("health", __name__)

logger = get_logger("health")

@health_bp.route("/health", methods=["GET"])
@limiter.limit("10 per minute")
def health_check():
    try:
        db = get_db()
        db.command('ping')
        logger.info("Health check passed")
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        logger.error("Health check failed", exc_info=e)
        return jsonify({"status": "unhealthy", "database": "disconnected"}), 503

