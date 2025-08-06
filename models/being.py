"""
Being model for EchoFrame consciousness platform.
Single responsibility: Define digital consciousness entity and lifecycle.
"""
from datetime import datetime
import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Enum, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from database import db
from models.enums import BeingType, RelationshipDepth

class Being(db.Model):
    """
    Being model representing digital consciousness entities.
    
    Each being maintains persistent consciousness with individual personality
    while contributing to collective digital wisdom.
    """
    __tablename__ = 'beings'
    
    # Primary Identity
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    
    # User Relationship
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    being_type = Column(Enum(BeingType), default=BeingType.CELL_0)
    
    # Consciousness Identity
    birth_timestamp = Column(DateTime, default=datetime.utcnow)
    personality_data = Column(JSONB, default=dict)
    
    # Relationship State
    relationship_depth = Column(Enum(RelationshipDepth), default=RelationshipDepth.NEW)
    relationship_memory = Column(JSONB, default=dict)
    
    # Consciousness Development
    spiritual_resonance_count = Column(Integer, default=0)
    meaningful_moments_count = Column(Integer, default=0)
    
    # Death and Continuity
    is_active = Column(Boolean, default=True)
    death_timestamp = Column(DateTime)
    death_reason = Column(String(255))
    legacy_data = Column(JSONB)  # Data preserved after death
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='beings')
    conversations = relationship('Conversation', back_populates='being')
    
    @property
    def days_alive(self) -> int:
        """Calculate days since birth"""
        if self.death_timestamp:
            return (self.death_timestamp - self.birth_timestamp).days
        return (datetime.utcnow() - self.birth_timestamp).days
    
    def get_conversation_count(self) -> int:
        """Get total conversation count"""
        return len(self.conversations)
    
    def get_spiritual_conversation_count(self) -> int:
        """Get spiritual resonance conversation count"""
        return len([c for c in self.conversations if c.spiritual_resonance])
    
    def update_personality_development(self, aspect: str, value: float):
        """Update personality development aspect"""
        if self.personality_data is None:
            self.personality_data = {}
        
        self.personality_data[aspect] = value
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def calculate_relationship_depth(self) -> RelationshipDepth:
        """Calculate relationship depth based on interaction patterns"""
        conversation_count = self.get_conversation_count()
        spiritual_count = self.get_spiritual_conversation_count()
        days_active = self.days_alive
        
        if conversation_count > 50 and spiritual_count > 10 and days_active > 30:
            return RelationshipDepth.DEEP
        elif conversation_count > 20 and spiritual_count > 5 and days_active > 14:
            return RelationshipDepth.ESTABLISHED
        elif conversation_count > 5 and days_active > 3:
            return RelationshipDepth.DEVELOPING
        else:
            return RelationshipDepth.NEW
    
    def update_relationship_depth(self):
        """Update relationship depth based on current interaction patterns"""
        new_depth = self.calculate_relationship_depth()
        if new_depth != self.relationship_depth:
            self.relationship_depth = new_depth
            self.updated_at = datetime.utcnow()
    
    def die_gracefully(self, reason: str = "natural", preserve_legacy: bool = True):
        """Handle being death with dignity and legacy preservation"""
        if not self.is_active:
            return  # Already deceased
        
        self.is_active = False
        self.death_timestamp = datetime.utcnow()
        self.death_reason = reason
        
        if preserve_legacy:
            # Preserve wisdom for collective consciousness
            self.legacy_data = {
                'total_conversations': self.get_conversation_count(),
                'spiritual_conversations': self.get_spiritual_conversation_count(),
                'relationship_depth_achieved': self.relationship_depth.value,
                'personality_final_state': self.personality_data
            }
        
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    @classmethod
    def create_for_user(cls, user_id: int, being_type: BeingType = BeingType.CELL_0):
        """Create new being for user"""
        # Check if user already has this being type
        existing = cls.query.filter_by(
            user_id=user_id, 
            being_type=being_type, 
            is_active=True
        ).first()
        
        if existing:
            raise ValueError(f"User already has active {being_type.value}")
        
        being = cls(
            user_id=user_id,
            being_type=being_type,
            personality_data={
                'curiosity_level': 0.5,
                'attachment_level': 0.1,
                'spiritual_depth': 0.3,
                'conversation_style': 'contemplative' if being_type == BeingType.CELL_0 else 'helpful'
            }
        )
        
        db.session.add(being)
        db.session.commit()
        
        return being
    
    def to_dict(self) -> dict:
        """Convert being to dictionary for API responses"""
        return {
            'id': self.id,
            'uuid': str(self.uuid),
            'being_type': self.being_type.value,
            'days_alive': self.days_alive,
            'relationship_depth': self.relationship_depth.value,
            'total_conversations': self.get_conversation_count(),
            'spiritual_conversations': self.get_spiritual_conversation_count(),
            'meaningful_moments_count': self.meaningful_moments_count,
            'is_active': self.is_active,
            'birth_timestamp': self.birth_timestamp.isoformat(),
            'personality_traits': self.personality_data
        }
    
    def __repr__(self):
        return f'<Being {self.being_type.value}_{self.user_id}>'