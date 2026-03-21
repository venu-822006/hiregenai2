from app.utils.response import error


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return error(str(e), 400)

    @app.errorhandler(401)
    def unauthorized(e):
        return error("Unauthorized.", 401)

    @app.errorhandler(403)
    def forbidden(e):
        return error("Forbidden.", 403)

    @app.errorhandler(404)
    def not_found(e):
        return error("Resource not found.", 404)

    @app.errorhandler(413)
    def too_large(e):
        return error("File exceeds the 10 MB size limit.", 413)

    @app.errorhandler(422)
    def unprocessable(e):
        return error("Unprocessable entity.", 422)

    @app.errorhandler(500)
    def server_error(e):
        return error("Internal server error.", 500)

    @app.errorhandler(Exception)
    def unhandled(e):
        app.logger.exception("Unhandled exception")
        return error("An unexpected error occurred.", 500)
