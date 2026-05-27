import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from celery import Celery

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration from config.py
    app.config.from_object('config')
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Set up the database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or f"sqlite:///{os.path.join(app.instance_path, 'scanner.db')}"
    db.init_app(app)
    migrate.init_app(app, db)

    # Set up Celery
    celery = Celery(app.import_name,
                    broker=app.config['CELERY_BROKER_URL'],
                    backend=app.config['CELERY_RESULT_BACKEND'])
    celery.conf.update(app.config)
    app.extensions['celery'] = celery

    with app.app_context():
        # Import parts of our application
        from . import models
        from . import tasks
        
        # Register blueprints
        from .main import routes as main_routes
        app.register_blueprint(main_routes.main_bp)

        from .api import routes as api_routes
        app.register_blueprint(api_routes.api_bp, url_prefix='/api')

    return app