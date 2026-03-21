from datetime import datetime, timezone


def job_schema(user_id: str, title: str, company: str, description: str, industry: str) -> dict:
    return {
        "user_id": user_id,
        "title": title,
        "company": company,
        "description": description,
        "industry": industry,
        "created_at": datetime.now(timezone.utc),
    }


def serialize_job(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "user_id": doc.get("user_id"),
        "title": doc.get("title"),
        "company": doc.get("company"),
        "description": doc.get("description"),
        "industry": doc.get("industry"),
        "created_at": doc["created_at"].isoformat() if isinstance(doc.get("created_at"), datetime) else doc.get("created_at"),
    }
