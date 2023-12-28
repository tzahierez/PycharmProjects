# # app/__init__.py
#
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from app.routes.task_routes import tasks_bp
#
# #app = Flask(__name__)
# app.register_blueprint(tasks_bp)
# # Replace 'todo-list' with the actual username, 'pass' with the actual password, and 'todo_db' with your actual database name.
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://todo-list:pass@localhost/todo_db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # to silence the deprecation warning
#
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
#
# # Import models here to ensure they are known to Flask-Migrate before running migrations
# from app.models import Task
#
# # Other parts of your Flask app initialization go here

# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.exam_routes import exam_routes
    from app.routes.person_routes import person_routes
    app.register_blueprint(exam_routes, url_prefix='/exam')
    app.register_blueprint(person_routes, url_prefix='/person')

    # Import models here to ensure they are known to Flask-Migrate before running migrations from app.models import Task

    return app
