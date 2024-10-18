from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name="default"):
    app = Flask(__name__)

    # Load config based on environment using object-based configuration
    from app.config import config  # Assuming you have a config.py with object-based configuration
    app.config.from_object(config[config_name])

    # Initialize extensions (SQLAlchemy)
    db.init_app(app)

    # Import and register blueprints (routes)
    from app import routes
    app.register_blueprint(routes.bp)

    # Register error handlers
    register_error_handlers(app)

    # Automatically create database tables (only in development)
    if config_name == 'development':
        with app.app_context():
            db.create_all()

    return app

def register_error_handlers(app):
    # Define error handlers for common HTTP errors (e.g., 404, 500)
    @app.errorhandler(404)
    def not_found_error(error):
        return "Page not found (404)", 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Roll back in case of database errors
        return "Internal server error (500)", 500
