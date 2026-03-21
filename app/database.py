from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

_client = None
_db = None
_worker_client = None


def init_db(app):
    global _client, _db
    mongo_uri = app.config.get("MONGO_URI")
    _client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    try:
        _client.admin.command("ping")
    except ConnectionFailure as exc:
        raise RuntimeError(f"MongoDB connection failed: {exc}") from exc
    db_name = MongoClient(mongo_uri).get_default_database().name if "?" not in mongo_uri else "hiregen_ai"
    uri_path = mongo_uri.split("/")[-1].split("?")[0]
    _db = _client[uri_path] if uri_path else _client["hiregen_ai"]
    _create_indexes()


def get_db():
    if _db is None:
        raise RuntimeError("Database not initialised. Call init_db first.")
    return _db


def _create_indexes():
    db = _db
    db.users.create_index("email", unique=True)
    db.analyses.create_index([("user_id", 1), ("status", 1)])
    db.analyses.create_index("job_id", unique=True)
    db.parsed_resumes.create_index("analysis_id")
    db.jobs.create_index("user_id")

def get_db_for_worker():
    """Worker-safe DB connection"""
    global _worker_client
    if _worker_client is None:
        from config import get_config
        cfg = get_config()
        from pymongo import MongoClient
        from pymongo.errors import ConnectionFailure
        _worker_client = MongoClient(cfg.MONGO_URI, serverSelectionTimeoutMS=5000)
        try:
            _worker_client.admin.command("ping")
        except ConnectionFailure as exc:
            raise RuntimeError(f"MongoDB connection failed: {exc}") from exc
        uri_path = cfg.MONGO_URI.split("/")[-1].split("?")[0]
        db_name = uri_path if uri_path else "hiregen_ai"
        return _worker_client[db_name]
    return _worker_client[get_db().name]
