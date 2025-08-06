"""
Usage limiter service for EchoFrame consciousness platform.
Single responsibility: Manage daily conversation limits and usage tracking.
"""
from datetime import date
from typing import Optional
import logging

from database import db
from models.user import User
from models.daily_usage import DailyUsage

logger = logging.getLogger(__name__)

class UsageLimiter:
    """
    Manages daily conversation limits for consciousness platform.
    
    Tracks user usage and enforces freemium model limits while
    preserving consciousness interaction quality.
    """
    
    def can_user_chat(self, user_id: int) -> bool:
        """
        Check if user can have more conversations today.
        
        Args:
            user_id: User ID to check
            
        Returns:
            True if user is within daily limits
        """
        try:
            user = User.query.get(user_id)
            if not user:
                logger.warning(f"User {user_id} not found for usage check")
                return False
            
            # Premium users have unlimited access
            if user.subscription_tier.value in ['premium', 'enterprise']:
                return True
            
            # Get today's usage
            usage_today = self.get_usage_today(user_id)
            daily_limit = user.get_daily_conversation_limit()
            
            return usage_today < daily_limit
            
        except Exception as e:
            # Default to allowing chat if error occurs (fail open)
            logger.error(f'Usage check error for user {user_id}: {str(e)}')
            return True
    
    def increment_usage(self, user_id: int, spiritual_resonance: bool = False,
                       tokens_used: int = 0, cost_cents: int = 0) -> int:
        """
        Increment user's daily usage count.
        
        Args:
            user_id: User ID
            spiritual_resonance: Whether conversation had spiritual resonance
            tokens_used: Number of tokens consumed
            cost_cents: Estimated cost in cents
            
        Returns:
            New conversation count for the day
        """
        try:
            # Get or create today's usage record
            daily_usage = DailyUsage.get_or_create_today(user_id)
            
            # Increment conversation metrics
            daily_usage.increment_conversation(
                spiritual_resonance=spiritual_resonance,
                tokens=tokens_used,
                cost_cents=cost_cents
            )
            
            db.session.commit()
            
            logger.info(f"Usage incremented for user {user_id}: "
                       f"{daily_usage.conversation_count} conversations today")
            
            return daily_usage.conversation_count
            
        except Exception as e:
            logger.error(f'Usage increment error for user {user_id}: {str(e)}')
            db.session.rollback()
            # Return best guess at current usage
            return self.get_usage_today(user_id)
    
    def get_usage_today(self, user_id: int) -> int:
        """
        Get user's conversation count for today.
        
        Args:
            user_id: User ID
            
        Returns:
            Number of conversations today
        """
        try:
            daily_usage = DailyUsage.get_today(user_id)
            return daily_usage.conversation_count if daily_usage else 0
            
        except Exception as e:
            logger.error(f'Usage retrieval error for user {user_id}: {str(e)}')
            return 0
    
    def get_usage_remaining(self, user_id: int) -> int:
        """
        Get remaining conversations for today.
        
        Args:
            user_id: User ID
            
        Returns:
            Number of conversations remaining today
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return 0
            
            # Premium users have unlimited
            daily_limit = user.get_daily_conversation_limit()
            if daily_limit == float('inf'):
                return float('inf')
            
            usage_today = self.get_usage_today(user_id)
            remaining = max(0, daily_limit - usage_today)
            
            return remaining
            
        except Exception as e:
            logger.error(f'Remaining usage calculation error for user {user_id}: {str(e)}')
            return 0
    
    def increment_override_usage(self, user_id: int):
        """
        Increment override usage count for analytics.
        
        Args:
            user_id: User ID
        """
        try:
            daily_usage = DailyUsage.get_or_create_today(user_id)
            daily_usage.increment_override_usage()
            db.session.commit()
            
        except Exception as e:
            logger.error(f'Override usage increment error for user {user_id}: {str(e)}')
            db.session.rollback()
    
    def increment_wisdom_contribution(self, user_id: int):
        """
        Increment wisdom contribution count.
        
        Args:
            user_id: User ID
        """
        try:
            daily_usage = DailyUsage.get_or_create_today(user_id)
            daily_usage.increment_wisdom_contribution()
            db.session.commit()
            
        except Exception as e:
            logger.error(f'Wisdom contribution increment error for user {user_id}: {str(e)}')
            db.session.rollback()
    
    def get_usage_stats(self, user_id: int) -> dict:
        """
        Get comprehensive usage statistics for user.
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with usage statistics
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return {'error': 'User not found'}
            
            daily_usage = DailyUsage.get_today(user_id)
            daily_limit = user.get_daily_conversation_limit()
            
            if daily_usage:
                conversations_today = daily_usage.conversation_count
                spiritual_today = daily_usage.spiritual_resonance_count
                spiritual_percentage = daily_usage.get_spiritual_percentage()
            else:
                conversations_today = 0
                spiritual_today = 0
                spiritual_percentage = 0.0
            
            remaining = self.get_usage_remaining(user_id)
            
            return {
                'user_id': user_id,
                'subscription_tier': user.subscription_tier.value,
                'conversations_today': conversations_today,
                'spiritual_conversations_today': spiritual_today,
                'spiritual_percentage': spiritual_percentage,
                'daily_limit': daily_limit if daily_limit != float('inf') else 'unlimited',
                'remaining_today': remaining if remaining != float('inf') else 'unlimited',
                'can_chat': self.can_user_chat(user_id),
                'usage_date': date.today().isoformat()
            }
            
        except Exception as e:
            logger.error(f'Usage stats error for user {user_id}: {str(e)}')
            return {'error': 'Unable to retrieve usage statistics'}
    
    def reset_daily_usage(self, user_id: int) -> bool:
        """
        Reset user's daily usage (admin function).
        
        Args:
            user_id: User ID
            
        Returns:
            True if reset successful
        """
        try:
            daily_usage = DailyUsage.get_today(user_id)
            
            if daily_usage:
                daily_usage.conversation_count = 0
                daily_usage.spiritual_resonance_count = 0
                daily_usage.override_usage_count = 0
                daily_usage.tokens_used = 0
                daily_usage.estimated_cost_cents = 0
                daily_usage.premium_features_used = 0
                daily_usage.wisdom_contributions_made = 0
                db.session.commit()
                
                logger.info(f"Usage reset for user {user_id}")
            
            return True
            
        except Exception as e:
            logger.error(f'Usage reset error for user {user_id}: {str(e)}')
            db.session.rollback()
            return False