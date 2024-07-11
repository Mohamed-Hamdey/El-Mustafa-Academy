from app.routes.auth import bp as auth_bp
from app.routes.courses import bp as courses_bp
from app.routes.assignments import bp as assignments_bp
from app.routes.exams import bp as exams_bp
from app.routes.videos import bp as videos_bp
from app.routes.enviroment import bp as environment_bp
from app.routes.schedule import bp as schedule_bp
from app.routes.notifications import bp as notifications_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(assignments_bp)
    app.register_blueprint(exams_bp)
    app.register_blueprint(videos_bp)
    app.register_blueprint(environment_bp)
    app.register_blueprint(schedule_bp)
    app.register_blueprint(notifications_bp)
