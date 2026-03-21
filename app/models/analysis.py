from datetime import datetime, timezone


def analysis_schema(
    user_id: str,
    job_id: str,
    job_title: str,
    industry: str,
    experience_level: str,
    job_description: str,
    status: str = "processing",
) -> dict:
    return {
        "user_id": user_id,
        "job_id": job_id,
        "job_title": job_title,
        "industry": industry,
        "experience_level": experience_level,
        "job_description": job_description,
        "status": status,
        "score": None,
        "verdict": None,
        "subscores": {},
        "skills": [],
        "ai_roles": [],
        "ai_experience_level": "",
        "keywords": {"found": [], "partial": [], "missing": []},
        "recommendations": [],
        "ai_suggestions": [],
        "hybrid_skills": [],
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }


def serialize_analysis(doc: dict) -> dict:
    return {
        "analysis_id": str(doc["_id"]),
        "job_id": doc.get("job_id"),
        "status": doc.get("status"),
        "score": doc.get("score"),
        "verdict": doc.get("verdict"),
        "subscores": doc.get("subscores", {}),
        "skills": doc.get("skills", []),
        "ai_roles": doc.get("ai_roles", []),
        "ai_experience_level": doc.get("ai_experience_level", ""),
        "hybrid_skills": doc.get("hybrid_skills", []),
        "keywords": doc.get("keywords", {"found": [], "partial": [], "missing": []}),
        "recommendations": doc.get("recommendations", []),
        "ai_suggestions": doc.get("ai_suggestions", []),
        "job_title": doc.get("job_title"),
        "industry": doc.get("industry"),
        "experience_level": doc.get("experience_level"),
        "created_at": doc["created_at"].isoformat() if isinstance(doc.get("created_at"), datetime) else doc.get("created_at"),
    }
