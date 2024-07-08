from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from .routes import auth, courses, assignments, exams, videos, environment, schedule, notifications
    app.register_blueprint(auth.bp)
    app.register_blueprint(courses.bp)
    app.register_blueprint(assignments.bp)
    app.register_blueprint(exams.bp)
    app.register_blueprint(videos.bp)
    app.register_blueprint(environment.bp)
    app.register_blueprint(schedule.bp)
    app.register_blueprint(notifications.bp)

    return app