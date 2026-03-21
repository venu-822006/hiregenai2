from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.utils.logger import get_logger
from config import get_config
from app.database import init_db
from app.errors.handlers import register_error_handlers
from app.routes.auth import auth_bp
from app.routes.analysis import analysis_bp
from app.routes.history import history_bp
from app.routes.ats import ats_bp
from app.routes.job_match import job_match_bp
from app.routes.resume_gen import resume_gen_bp
from app.routes.health import health_bp
from app.middleware.rate_limiter import limiter

limiter = Limiter(key_func=get_remote_address)
def create_app():
    from app.middleware.rate_limiter import limiter   # ✅ ADD HERE

    app = Flask(__name__)

    cfg = get_config()
    app.config.from_object(cfg)

    # ✅ INIT LIMITER HERE
    limiter.init_app(app)

    return app

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    logger = get_logger("app")
    app.logger = logger

    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri=cfg.RATELIMIT_STORAGE_URL
    )

    init_db(app)

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(analysis_bp, url_prefix="/api/v1")
    app.register_blueprint(history_bp, url_prefix="/api/v1")
    app.register_blueprint(ats_bp, url_prefix="/api/v1")
    app.register_blueprint(job_match_bp, url_prefix="/api/v1")
    app.register_blueprint(resume_gen_bp, url_prefix="/api/v1")
    app.register_blueprint(health_bp, url_prefix="/api/v1")

    register_error_handlers(app)

    return app
