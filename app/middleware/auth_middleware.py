from functools import wraps
from flask import request, g
import jwt as pyjwt

from app.utils.jwt_utils import decode_token
from app.utils.response import error
from app.database import get_db
from bson import ObjectId


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return error("Missing or malformed Authorization header.", 401)
        token = auth_header.split(" ", 1)[1]
        try:
            payload = decode_token(token)
        except pyjwt.ExpiredSignatureError:
            return error("Token has expired.", 401)
        except pyjwt.InvalidTokenError:
            return error("Invalid token.", 401)

        if payload.get("type") != "access":
            return error("Invalid token type.", 401)

        db = get_db()
        user = db.users.find_one({"_id": ObjectId(payload["sub"])})
        if not user:
            return error("User not found.", 401)

        g.user_id = str(user["_id"])
        g.user_role = user.get("role", "user")
        g.user = user
        return f(*args, **kwargs)

    return decorated


def require_admin(f):
    @wraps(f)
    @require_auth
    def decorated(*args, **kwargs):
        if g.user_role != "admin":
            return error("Admin access required.", 403)
        return f(*args, **kwargs)

    return decorated
