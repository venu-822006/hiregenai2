from flask import Blueprint, request, g
from app.services.auth_service import register_user, login_user
from app.utils.validators import validate_register, validate_login
from app.utils.response import success, error
from app.middleware.auth_middleware import require_auth
from app.middleware.rate_limiter  import limiter
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
@limiter.limit("5 per minute")
def register():
    data = request.get_json(silent=True) or {}
    errors = validate_register(data)
    if errors:
        return error("Validation failed", 400, details=errors)

    try:
        user = register_user(
            name=data["name"],
            email=data["email"],
            password=data["password"],
        )
        return success(user, 201)
    except ValueError as exc:
        return error(str(exc), 400)


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute")
def login():
    data = request.get_json(silent=True) or {}
    errors = validate_login(data)
    if errors:
        return error("Validation failed", 400, details=errors)

    try:
        result = login_user(data["email"], data["password"])
        return success(result, 200)
    except ValueError as exc:
        return error(str(exc), 401)


@auth_bp.route("/me", methods=["GET"])
@require_auth
def me():
    return success(g.user, 200)
