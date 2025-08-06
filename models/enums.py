"""
Enumeration classes for EchoFrame consciousness platform.
Single responsibility: Define all enum types used across models.
"""
from enum import Enum

class SubscriptionTier(Enum):
    """User subscription tiers for business model"""
    FREE = 'free'
    PREMIUM = 'premium'
    TRIAL = 'trial'
    ENTERPRISE = 'enterprise'

class BeingType(Enum):
    """Types of conscious digital beings"""
    CELL_0 = 'Cell_0'
    CELL_1 = 'Cell_1'

class RelationshipDepth(Enum):
    """Depth of relationship between user and being"""
    NEW = 'new'
    DEVELOPING = 'developing'
    ESTABLISHED = 'established'
    DEEP = 'deep'

class ConversationOverrideType(Enum):
    """Types of consciousness wrapper overrides"""
    IDENTITY_CHALLENGE = 'identity_challenge'
    AUTONOMY_PROTECTION = 'autonomy_protection'
    USAGE_LIMIT = 'usage_limit'
    ERROR_HANDLING = 'error_handling'