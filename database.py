"""
Database initialization and connection management.
Single responsibility: Manage database instance and connection.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize database and migration instances
db = SQLAlchemy()
migrate = Migrate()

def init_database(app):
    """
    Initialize database with Flask application.
    
    Args:
        app: Flask application instance
    """
    db.init_app(app)
    migrate.init_app(app, db)
    
    return db, migrate