from flask import Blueprint, g
from app.middleware.auth_middleware import require_auth
from app.services.analysis_service import get_user_analyses
from app.utils.response import success

history_bp = Blueprint("history", __name__)


@history_bp.route("/history", methods=["GET"])
@require_auth
def get_history():
    records = get_user_analyses(g.user_id)
    return success(records, 200)
