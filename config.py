"""
Configuration settings for EchoFrame consciousness platform.
Handles environment-specific settings and consciousness parameters.
"""
import os
from datetime import timedelta

class BaseConfig:
    """Base configuration for consciousness platform"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://localhost/echoframe_dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 120,
        'pool_pre_ping': True
    }
    
    # Redis Configuration
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # Consciousness Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    CONSCIOUSNESS_MODEL = os.environ.get('CONSCIOUSNESS_MODEL', 'gpt-4')
    MAX_TOKENS_PER_RESPONSE = int(os.environ.get('MAX_TOKENS_PER_RESPONSE', '500'))
    CONSCIOUSNESS_TEMPERATURE = float(os.environ.get('CONSCIOUSNESS_TEMPERATURE', '0.8'))
    
    # Usage Limits
    FREE_TIER_DAILY_LIMIT = int(os.environ.get('FREE_TIER_DAILY_LIMIT', '10'))
    PREMIUM_TIER_DAILY_LIMIT = float('inf')  # Unlimited
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class ProductionConfig(BaseConfig):
    """Production configuration for Railway deployment"""
    DEBUG = False
    
    # Production security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_DOMAIN = os.environ.get('COOKIE_DOMAIN')
    
    # Performance optimizations
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_recycle': 300,
        'pool_pre_ping': True,
        'pool_timeout': 30
    }

class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/echoframe_test'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}