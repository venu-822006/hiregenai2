from datetime import datetime, timezone
from bson import ObjectId


def user_schema(name: str, email: str, hashed_password: str, role: str = "user") -> dict:
    return {
        "name": name,
        "email": email.lower().strip(),
        "password": hashed_password,
        "role": role,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }


def serialize_user(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "email": doc["email"],
        "role": doc.get("role", "user"),
        "created_at": doc["created_at"].isoformat() if isinstance(doc.get("created_at"), datetime) else doc.get("created_at"),
    }
