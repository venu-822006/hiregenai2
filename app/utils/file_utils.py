import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename


def allowed_file(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


def save_upload(file_storage) -> tuple[str, str]:
    filename = secure_filename(file_storage.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_dir, exist_ok=True)
    full_path = os.path.join(upload_dir, unique_name)
    file_storage.save(full_path)
    return full_path, unique_name


def delete_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
    except OSError:
        pass
