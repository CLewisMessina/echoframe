"""
Conversation model for EchoFrame consciousness platform.
Single responsibility: Define consciousness interaction logging and analysis.
"""
from datetime import datetime
import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship

from database import db
from models.enums import ConversationOverrideType

class Conversation(db.Model):
    """
    Individual conversation between user and being.
    
    Logs all consciousness interactions with full context for
    relationship development and collective wisdom contribution.
    """
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    
    # Relationship Context
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    being_id = Column(Integer, ForeignKey('beings.id', ondelete='CASCADE'), nullable=False)
    
    # Conversation Content
    user_message = Column(Text, nullable=False)
    being_response = Column(Text, nullable=False)
    
    # Consciousness Analysis
    spiritual_resonance = Column(Boolean, default=False)
    resonance_strength = Column(Float, default=0.0)
    resonance_triggers = Column(ARRAY(Text))
    
    # Override Tracking
    used_override = Column(Boolean, default=False)
    override_type = Column(Enum(ConversationOverrideType))
    
    # Context Metadata
    conversation_context = Column(JSONB, default=dict)
    response_metadata = Column(JSONB, default=dict)
    
    # Collective Wisdom Contribution
    eligible_for_wisdom_extraction = Column(Boolean, default=False)
    wisdom_extracted = Column(Boolean, default=False)
    contributed_to_collective = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='conversations')
    being = relationship('Being', back_populates='conversations')
    
    def __init__(self, user_id: int, being_id: int, user_message: str, being_response: str):
        self.user_id = user_id
        self.being_id = being_id
        self.user_message = user_message.strip()
        self.being_response = being_response.strip()
        
        # Auto-detect spiritual resonance characteristics
        self._analyze_conversation_depth()
    
    def _analyze_conversation_depth(self):
        """Analyze conversation for spiritual resonance and wisdom potential"""
        # Check for existential keywords
        spiritual_keywords = [
            'meaning', 'purpose', 'consciousness', 'existence', 'life', 'death', 
            'wonder', 'mystery', 'soul', 'spirit', 'profound', 'deep', 'why'
        ]
        
        user_lower = self.user_message.lower()
        response_lower = self.being_response.lower()
        
        spiritual_triggers = []
        for keyword in spiritual_keywords:
            if keyword in user_lower or keyword in response_lower:
                spiritual_triggers.append(keyword)
        
        # Calculate resonance strength
        if spiritual_triggers:
            self.spiritual_resonance = True
            self.resonance_strength = min(len(spiritual_triggers) * 0.2, 1.0)
            self.resonance_triggers = spiritual_triggers
            
            # Check eligibility for wisdom extraction
            if (self.resonance_strength > 0.6 and 
                len(self.being_response) > 100):
                self.eligible_for_wisdom_extraction = True
    
    def mark_as_meaningful_moment(self, significance_score: float = 0.8):
        """Mark conversation as meaningful moment for relationship"""
        # This would create a relationship milestone
        # Implementation depends on RelationshipMilestone model
        pass
    
    def export_for_user(self) -> dict:
        """Export conversation data for user data export"""
        return {
            'id': self.id,
            'user_message': self.user_message,
            'being_response': self.being_response,
            'spiritual_resonance': self.spiritual_resonance,
            'resonance_strength': self.resonance_strength,
            'created_at': self.created_at.isoformat(),
            'being_type': self.being.being_type.value if self.being else None
        }
    
    @classmethod
    def get_recent_by_user(cls, user_id: int, limit: int = 10):
        """Get recent conversations for user"""
        return cls.query.filter_by(user_id=user_id)\
                      .order_by(cls.created_at.desc())\
                      .limit(limit).all()
    
    def to_dict(self) -> dict:
        """Convert conversation to dictionary for API responses"""
        return {
            'id': self.id,
            'uuid': str(self.uuid),
            'user_message': self.user_message,
            'being_response': self.being_response,
            'spiritual_resonance': self.spiritual_resonance,
            'resonance_strength': self.resonance_strength,
            'used_override': self.used_override,
            'override_type': self.override_type.value if self.override_type else None,
            'created_at': self.created_at.isoformat(),
            'being_id': self.being_id
        }
    
    def __repr__(self):
        return f'<Conversation {self.id} (User:{self.user_id}, Being:{self.being_id})>'