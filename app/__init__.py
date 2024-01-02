

# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from app.routes.ocr_routes import ocr_routes

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.exam_routes import exam_routes
    from app.routes.person_routes import person_routes
    from app.routes.playground_routes import playground_routes
    app.register_blueprint(exam_routes, url_prefix='/exam')
    app.register_blueprint(person_routes, url_prefix='/person')
    app.register_blueprint(playground_routes, url_prefix='/playground')
    app.register_blueprint(ocr_routes, url_prefix='/ocr')

    # Import models here to ensure they are known to Flask-Migrate before running migrations from app.models import Task

    return app
