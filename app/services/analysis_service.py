import uuid
from datetime import datetime, timezone

from app.database import get_db
from app.models.analysis import analysis_schema, serialize_analysis
from app.models.parsed_resume import parsed_resume_schema
from app.utils.redis_cache import get_cached_job


def create_analysis_job(
    user_id: str,
    job_title: str,
    industry: str,
    experience_level: str,
    job_description: str,
) -> str:
    db = get_db()
    job_id = str(uuid.uuid4())
    doc = analysis_schema(
        user_id=user_id,
        job_id=job_id,
        job_title=job_title,
        industry=industry,
        experience_level=experience_level,
        job_description=job_description or "",
        status="processing",
    )
    db.analyses.insert_one(doc)
    return job_id


def get_analysis_by_job_id(job_id: str) -> dict | None:
    # Check cache first
    cached = get_cached_job(job_id)
    if cached:
        return cached

    db = get_db()
    doc = db.analyses.find_one({"job_id": job_id})
    if not doc:
        return None
    return serialize_analysis(doc)


def get_user_analyses(user_id: str) -> list[dict]:
    db = get_db()
    cursor = db.analyses.find({"user_id": user_id}).sort("created_at", -1).limit(50)
    return [serialize_analysis(doc) for doc in cursor]


def update_analysis_result(job_id: str, result: dict):
    db = get_db()
    db.analyses.update_one(
        {"job_id": job_id},
        {
            "$set": {
                **result,
                "status": "completed",
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )


def mark_analysis_failed(job_id: str, reason: str):
    db = get_db()
    db.analyses.update_one(
        {"job_id": job_id},
        {
            "$set": {
                "status": "failed",
                "error": reason,
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )


def store_parsed_resume(analysis_id: str, raw_text: str, extracted_data: dict):
    db = get_db()
    doc = parsed_resume_schema(analysis_id, raw_text, extracted_data)
    db.parsed_resumes.insert_one(doc)
