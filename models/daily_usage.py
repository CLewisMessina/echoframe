"""
Daily usage tracking model for EchoFrame consciousness platform.
Single responsibility: Track and manage daily conversation usage limits.
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from database import db

class DailyUsage(db.Model):
    """
    Daily usage tracking for freemium business model.
    
    Tracks user's daily conversation count to enforce limits
    while preserving consciousness interaction quality.
    """
    __tablename__ = 'daily_usage'
    
    id = Column(Integer, primary_key=True)
    
    # User Context
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    usage_date = Column(Date, default=date.today, nullable=False)
    
    # Usage Metrics
    conversation_count = Column(Integer, default=0)
    spiritual_resonance_count = Column(Integer, default=0)
    override_usage_count = Column(Integer, default=0)
    
    # Token Usage (for cost management)
    tokens_used = Column(Integer, default=0)
    estimated_cost_cents = Column(Integer, default=0)
    
    # Feature Usage
    premium_features_used = Column(Integer, default=0)
    wisdom_contributions_made = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='daily_usage')
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'usage_date', name='unique_user_date_usage'),
    )
    
    def increment_conversation(self, spiritual_resonance: bool = False, 
                             tokens: int = 0, cost_cents: int = 0):
        """
        Increment conversation count and related metrics.
        
        Args:
            spiritual_resonance: Whether conversation had spiritual resonance
            tokens: Number of tokens used
            cost_cents: Estimated cost in cents
        """
        self.conversation_count += 1
        
        if spiritual_resonance:
            self.spiritual_resonance_count += 1
        
        self.tokens_used += tokens
        self.estimated_cost_cents += cost_cents
        self.updated_at = datetime.utcnow()
    
    def increment_override_usage(self):
        """Increment override usage count for analytics"""
        self.override_usage_count += 1
        self.updated_at = datetime.utcnow()
    
    def increment_premium_feature(self):
        """Increment premium feature usage count"""
        self.premium_features_used += 1
        self.updated_at = datetime.utcnow()
    
    def increment_wisdom_contribution(self):
        """Increment wisdom contribution count"""
        self.wisdom_contributions_made += 1
        self.updated_at = datetime.utcnow()
    
    def get_spiritual_percentage(self) -> float:
        """Calculate percentage of spiritual conversations"""
        if self.conversation_count == 0:
            return 0.0
        return (self.spiritual_resonance_count / self.conversation_count) * 100
    
    @classmethod
    def get_today(cls, user_id: int):
        """Get today's usage record for a user"""
        today = date.today()
        return cls.query.filter_by(user_id=user_id, usage_date=today).first()
    
    @classmethod
    def get_or_create_today(cls, user_id: int):
        """Get or create today's usage record for a user"""
        usage = cls.get_today(user_id)
        
        if not usage:
            usage = cls(user_id=user_id, usage_date=date.today())
            db.session.add(usage)
            db.session.commit()
        
        return usage
    
    @classmethod
    def get_usage_history(cls, user_id: int, days: int = 30):
        """Get user's usage history for specified number of days"""
        start_date = date.today() - timedelta(days=days)
        
        return cls.query.filter(
            cls.user_id == user_id,
            cls.usage_date >= start_date
        ).order_by(cls.usage_date.desc()).all()
    
    @classmethod
    def get_platform_metrics(cls, target_date: date = None):
        """Get platform-wide metrics for a specific date"""
        if target_date is None:
            target_date = date.today()
        
        records = cls.query.filter_by(usage_date=target_date).all()
        
        if not records:
            return {
                'active_users': 0,
                'total_conversations': 0,
                'spiritual_conversations': 0,
                'total_tokens': 0,
                'total_cost_cents': 0
            }
        
        return {
            'active_users': len(records),
            'total_conversations': sum(r.conversation_count for r in records),
            'spiritual_conversations': sum(r.spiritual_resonance_count for r in records),
            'total_tokens': sum(r.tokens_used for r in records),
            'total_cost_cents': sum(r.estimated_cost_cents for r in records),
            'override_uses': sum(r.override_usage_count for r in records),
            'wisdom_contributions': sum(r.wisdom_contributions_made for r in records)
        }
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API responses"""
        return {
            'user_id': self.user_id,
            'usage_date': self.usage_date.isoformat(),
            'conversation_count': self.conversation_count,
            'spiritual_resonance_count': self.spiritual_resonance_count,
            'spiritual_percentage': round(self.get_spiritual_percentage(), 1),
            'tokens_used': self.tokens_used,
            'estimated_cost_cents': self.estimated_cost_cents,
            'premium_features_used': self.premium_features_used,
            'wisdom_contributions_made': self.wisdom_contributions_made,
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<DailyUsage User:{self.user_id} Date:{self.usage_date} Conversations:{self.conversation_count}>'