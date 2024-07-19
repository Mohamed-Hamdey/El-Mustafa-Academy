from app.routes.auth import bp as auth_bp
from app.routes.assignments import bp as assignments_bp
from app.routes.exams import bp as exams_bp
from app.routes.videos import bp as videos_bp
from app.routes.grades import bp as grades_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(assignments_bp)
    app.register_blueprint(exams_bp)
    app.register_blueprint(videos_bp)
    app.register_blueprint(grades_bp, url_prefix='/grades')

