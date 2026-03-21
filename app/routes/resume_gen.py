from flask import Blueprint, request
from app.middleware.auth_middleware import require_auth
from app.utils.response import success, error

resume_gen_bp = Blueprint("resume_gen", __name__)


@resume_gen_bp.route("/generate-resume", methods=["POST"])
@require_auth
def generate_resume():
    """
    Placeholder for resume generation logic.
    In a full implementation, this might take user profile data and use an AI model
    or template engine to produce a PDF/DOCX.
    """
    data = request.get_json(silent=True) or {}
    job_title = data.get("job_title")

    if not job_title:
        return error("job_title is required for resume generation.", 400)

    return success(
        {
            "message": "Resume generation initiated.",
            "generated_link": f"https://example.com/resumes/generated_{job_title.replace(' ', '_').lower()}.pdf",
        },
        200,
    )
