import re
import html


EMAIL_RE = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def sanitize_string(value: str) -> str:
    """Strip whitespace and escape HTML."""
    return html.escape(value.strip())


def validate_register(data: dict) -> list[str]:
    errors = []
    name = data.get("name", "").strip()
    if not name or len(name) < 2 or len(name) > 100:
        errors.append("name must be 2-100 characters.")
    email = data.get("email", "").strip().lower()
    if not email or not EMAIL_RE.match(email) or len(email) > 254:
        errors.append("A valid email (max 254 chars) is required.")
    password = data.get("password", "")
    if not password or len(password) < 8 or len(password) > 128:
        errors.append("password must be 8-128 characters.")
    # Sanitize
    data["name"] = sanitize_string(data.get("name", ""))
    data["email"] = email
    return errors


def validate_login(data: dict) -> list[str]:
    errors = []
    email = data.get("email", "").strip().lower()
    if not email or not EMAIL_RE.match(email):
        errors.append("A valid email is required.")
    if not data.get("password"):
        errors.append("password is required.")
    # Sanitize
    data["email"] = email
    return errors


def validate_analysis(data: dict, has_file: bool) -> list[str]:
    errors = []
    cv_text = data.get("cv_text", "").strip()
    if not has_file and not cv_text:
        errors.append("Either a file upload or cv_text field is required.")
    if cv_text and len(cv_text) > 10000:
        errors.append("cv_text must be less than 10,000 characters.")
    job_title = data.get("job_title", "").strip()
    if not job_title or len(job_title) > 200:
        errors.append("job_title is required and must be less than 200 characters.")
    industry = data.get("industry", "").strip()
    if not industry or len(industry) > 100:
        errors.append("industry is required and must be less than 100 characters.")
    experience_level = data.get("experience_level", "").strip()
    if not experience_level or len(experience_level) > 50:
        errors.append("experience_level is required and must be less than 50 characters.")
    job_description = data.get("job_description", "").strip()
    if job_description and len(job_description) > 5000:
        errors.append("job_description must be less than 5,000 characters.")
    # Sanitize
    data["cv_text"] = sanitize_string(cv_text) if cv_text else ""
    data["job_title"] = sanitize_string(job_title)
    data["industry"] = sanitize_string(industry)
    data["experience_level"] = sanitize_string(experience_level)
    data["job_description"] = sanitize_string(job_description) if job_description else ""
    return errors
