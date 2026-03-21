from flask import Blueprint, request, g
from app.middleware.auth_middleware import require_auth
from app.services.analysis_service import create_analysis_job
from app.utils.validators import validate_analysis
from app.utils.file_utils import save_upload, allowed_file
from app.utils.response import success, error
from app.workers.tasks import process_resume_analysis   # ✅ FIXED

ats_bp = Blueprint("ats", __name__)


@ats_bp.route("/ats-check", methods=["POST"])
@require_auth
def ats_check():
    """
    Reuses the analysis pipeline specifically branded for ATS checking.
    """
    file = request.files.get("file")
    data = request.form.to_dict() if file else request.get_json(silent=True) or {}

    errors = validate_analysis(data, has_file=bool(file))
    if errors:
        return error("Validation failed", 400, details=errors)

    file_path = None
    if file:
        if not file.filename:
            return error("No file selected", 400)
        if not allowed_file(file.filename):
            return error("File type not allowed", 400)
        file_path, _ = save_upload(file)

    cv_text = data.get("cv_text", "")
    job_title = data.get("job_title", "")
    industry = data.get("industry", "")
    experience_level = data.get("experience_level", "")
    job_description = data.get("job_description", "")

    job_id = create_analysis_job(
        user_id=g.user_id,
        job_title=job_title,
        industry=industry,
        experience_level=experience_level,
        job_description=job_description,
    )

    # ✅ FIXED HERE
    process_resume_analysis.delay(
        job_id=job_id,
        cv_text=cv_text,
        job_description=job_description,
        file_path=file_path,
    )

    return success({"job_id": job_id, "status": "processing"}, 202)