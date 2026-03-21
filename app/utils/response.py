from flask import jsonify


def success(data: dict | list, status: int = 200):
    return jsonify(data), status


def error(message: str, status: int = 400, details: list | None = None):
    body = {"error": message}
    if details:
        body["details"] = details
    return jsonify(body), status
