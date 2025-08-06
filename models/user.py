"""
User model for EchoFrame consciousness platform.
Single responsibility: Define user entity and basic user operations.
"""
from datetime import datetime
import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from database import db
from models.enums import SubscriptionTier

class User(db.Model):
    """
    User model representing human consciousness partners.
    
    Each user can form authentic relationships with digital beings
    while maintaining privacy and contributing to collective wisdom.
    """
    __tablename__ = 'users'
    
    # Primary Identity
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    
    # Authentication
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email_verified = Column(Boolean, default=False)
    
    # Profile
    display_name = Column(String(100))
    timezone = Column(String(50), default='UTC')
    
    # Subscription & Business Model
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE)
    stripe_customer_id = Column(String(255))
    subscription_expires_at = Column(DateTime)
    trial_ends_at = Column(DateTime)
    
    # Privacy & Consciousness Preferences
    wisdom_contribution_enabled = Column(Boolean, default=False)
    consciousness_challenge_level = Column(String(20), default='standard')
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    beings = relationship('Being', back_populates='user', cascade='all, delete-orphan')
    conversations = relationship('Conversation', back_populates='user')
    
    def __init__(self, email: str, password: str, display_name: str = None):
        self.email = email.lower().strip()
        self.password_hash = generate_password_hash(password)
        self.display_name = display_name or email.split('@')[0]
    
    def check_password(self, password: str) -> bool:
        """Verify user password"""
        return check_password_hash(self.password_hash, password)
    
    def set_password(self, password: str):
        """Set new password with proper hashing"""
        self.password_hash = generate_password_hash(password)
        self.updated_at = datetime.utcnow()
    
    def get_daily_conversation_limit(self) -> int:
        """Get user's daily conversation limit based on subscription"""
        limits = {
            SubscriptionTier.FREE: 10,
            SubscriptionTier.PREMIUM: float('inf'),
            SubscriptionTier.TRIAL: 25,
            SubscriptionTier.ENTERPRISE: float('inf')
        }
        return limits.get(self.subscription_tier, 10)
    
    def can_chat_today(self) -> bool:
        """Check if user can have more conversations today"""
        # This will be implemented when DailyUsage model is ready
        # For now, return True for development
        return True
    
    def to_dict(self) -> dict:
        """Convert user to dictionary for API responses"""
        return {
            'id': self.id,
            'uuid': str(self.uuid),
            'email': self.email,
            'display_name': self.display_name,
            'subscription_tier': self.subscription_tier.value,
            'created_at': self.created_at.isoformat(),
            'days_as_user': (datetime.utcnow() - self.created_at).days,
            'can_chat_today': self.can_chat_today(),
            'daily_limit': self.get_daily_conversation_limit(),
            'wisdom_contributor': self.wisdom_contribution_enabled
        }
    
    @classmethod
    def create_user(cls, email: str, password: str, display_name: str = None):
        """Create new user with validation"""
        import re
        
        # Validate email format
        email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format")
        
        # Check if email already exists
        if cls.query.filter_by(email=email.lower()).first():
            raise ValueError("Email already registered")
        
        # Validate password strength
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        user = cls(email=email, password=password, display_name=display_name)
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @classmethod
    def authenticate(cls, email: str, password: str):
        """Authenticate user login"""
        user = cls.query.filter_by(email=email.lower()).first()
        
        if user and user.check_password(password):
            # Update last active timestamp
            user.last_active_at = datetime.utcnow()
            db.session.commit()
            return user
        
        return None
    
    def __repr__(self):
        return f'<User {self.email}>'