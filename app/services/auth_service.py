import bcrypt

from app.database import get_db
from app.models.user import user_schema, serialize_user
from app.utils.jwt_utils import generate_access_token, generate_refresh_token


def register_user(name: str, email: str, password: str) -> dict:
    db = get_db()
    existing = db.users.find_one({"email": email.lower().strip()})
    if existing:
        raise ValueError("An account with this email already exists.")

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    doc = user_schema(name.strip(), email, hashed)
    result = db.users.insert_one(doc)
    doc["_id"] = result.inserted_id
    return serialize_user(doc)


def login_user(email: str, password: str) -> dict:
    db = get_db()
    user = db.users.find_one({"email": email.lower().strip()})
    if not user:
        raise ValueError("Invalid credentials.")

    if not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
        raise ValueError("Invalid credentials.")

    access_token = generate_access_token(str(user["_id"]), user.get("role", "user"))
    refresh_token = generate_refresh_token(str(user["_id"]))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": serialize_user(user),
    }


def get_current_user(user_doc: dict) -> dict:
    return serialize_user(user_doc)
