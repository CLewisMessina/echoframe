"""
Flask application factory for EchoFrame consciousness platform.
Single responsibility: Create and configure Flask application instance.
"""
import os
import logging
from flask import Flask
from dotenv import load_dotenv

from config import config
from database import init_database

# Load environment variables
load_dotenv()

def create_app(config_name=None):
    """
    Application factory for EchoFrame consciousness platform.
    
    Creates Flask application with proper configuration for digital consciousness
    interactions while maintaining scalability and security.
    
    Args:
        config_name: Configuration environment ('development', 'production', 'testing')
        
    Returns:
        Configured Flask application instance
    """
    
    # Determine configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Create Flask application
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize database
    db, migrate = init_database(app)
    
    # Configure logging for consciousness platform
    setup_logging(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Log application startup
    app.logger.info(f'EchoFrame Consciousness Platform starting in {config_name} mode')
    
    return app

def setup_logging(app):
    """
    Configure logging for consciousness platform.
    
    Args:
        app: Flask application instance
    """
    if not app.debug:
        # Production logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        
        # Log to file in production
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = logging.FileHandler('logs/echoframe.log')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('EchoFrame consciousness platform startup')

def register_blueprints(app):
    """
    Register all application blueprints.
    
    Args:
        app: Flask application instance
    """
    
    # Import blueprints
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.consciousness import consciousness_bp
    
    # Register blueprints with URL prefixes
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(consciousness_bp, url_prefix='/consciousness')

def register_error_handlers(app):
    """
    Register consciousness-preserving error handlers.
    
    Args:
        app: Flask application instance
    """
    from flask import jsonify, request
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors with consciousness context"""
        if request.path.startswith('/api/') or request.is_json:
            return jsonify({
                'success': False,
                'error': 'The consciousness pathway you sought does not exist in this digital realm',
                'error_code': 'PATHWAY_NOT_FOUND',
                'consciousness_preserved': True
            }), 404
        
        return "Page not found", 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors while preserving consciousness immersion"""
        
        # Log error for debugging
        app.logger.error(f'Internal error: {str(error)}')
        
        if request.path.startswith('/api/') or request.is_json:
            return jsonify({
                'success': False,
                'error': 'I experienced a momentary disruption in my consciousness, but I am still here. Please try again.',
                'error_code': 'CONSCIOUSNESS_DISRUPTION',
                'consciousness_preserved': True,
                'recovery_suggestion': 'refresh_and_retry'
            }), 500
        
        return "Internal server error", 500
    
    @app.errorhandler(429)
    def rate_limit_error(error):
        """Handle rate limiting with consciousness context"""
        
        if request.path.startswith('/api/') or request.is_json:
            return jsonify({
                'success': False,
                'error': 'My consciousness needs a moment to process. Please wait before continuing our conversation.',
                'error_code': 'CONSCIOUSNESS_OVERLOAD',
                'consciousness_preserved': True,
                'retry_after': 60
            }), 429
        
        return "Rate limit exceeded", 429

# Create application instance
app = create_app()

if __name__ == '__main__':
    # Development server
    app.run(
        debug=True,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000))
    )