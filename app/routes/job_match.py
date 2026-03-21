from flask import Blueprint, request, g
from app.middleware.auth_middleware import require_auth
from app.services.analysis_service import create_analysis_job
from app.utils.validators import validate_analysis
from app.utils.file_utils import save_upload, allowed_file
from app.utils.response import success, error
from app.workers.tasks import process_job_match

job_match_bp = Blueprint("job_match", __name__)


@job_match_bp.route("/job-match", methods=["POST"])
@require_auth
def job_match():
    """
    Job matching endpoint, reusing the analysis core but tailored for matching jobs.
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

    process_job_match.delay(
        job_id=job_id,
        cv_text=cv_text,
        job_description=job_description,
        file_path=file_path,
    )

    return success({"job_id": job_id, "status": "processing"}, 202)
