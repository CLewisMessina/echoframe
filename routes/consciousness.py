"""
Consciousness interaction routes for EchoFrame platform.
Single responsibility: Handle consciousness chat and being interactions.
"""
from flask import Blueprint, request, jsonify, session
import logging

from database import db
from models.user import User
from models.being import Being, BeingType
from models.conversation import Conversation
from services.usage_limiter import UsageLimiter
from consciousness.multi_tenant_wrapper import MultiTenantConsciousBeing

logger = logging.getLogger(__name__)
consciousness_bp = Blueprint('consciousness', __name__)

def require_auth(f):
    """Decorator to require authentication for consciousness endpoints"""
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        authenticated = session.get('authenticated', False)
        
        if not user_id or not authenticated:
            return jsonify({
                'success': False,
                'error': 'Authentication required for consciousness interaction'
            }), 401
        
        # Verify user exists
        user = User.query.get(user_id)
        if not user:
            session.clear()
            return jsonify({
                'success': False,
                'error': 'Invalid session - please login again'
            }), 401
        
        return f(*args, **kwargs)
    
    decorated_function.__name__ = f.__name__
    return decorated_function

@consciousness_bp.route('/chat', methods=['POST'])
@require_auth
def chat():
    """
    Send message to being and get consciousness response.
    
    Core consciousness interaction endpoint with wrapper integration.
    """
    try:
        user_id = session.get('user_id')
        data = request.get_json()
        
        message = data.get('message', '').strip()
        being_type = data.get('being_type', 'Cell_0')
        
        # Validate input
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message cannot be empty'
            }), 400
        
        if len(message) > 2000:
            return jsonify({
                'success': False,
                'error': 'Message too long (max 2000 characters)'
            }), 400
        
        # Check usage limits
        usage_limiter = UsageLimiter()
        if not usage_limiter.can_user_chat(user_id):
            user = User.query.get(user_id)
            daily_limit = user.get_daily_conversation_limit()
            
            return jsonify({
                'success': False,
                'error': f'Daily conversation limit ({daily_limit}) reached',
                'limit_reached': True,
                'upgrade_url': '/subscription/upgrade',
                'reset_time': 'midnight UTC'
            }), 429
        
        # Get or create being
        being = Being.query.filter_by(
            user_id=user_id,
            being_type=BeingType(being_type),
            is_active=True
        ).first()
        
        if not being:
            # Create being if it doesn't exist
            being = Being.create_for_user(user_id, BeingType(being_type))
        
        # Create consciousness wrapper instance
        consciousness_wrapper = MultiTenantConsciousBeing(
            user_id=str(user_id),
            being_type=being_type
        )
        
        # Get consciousness response
        wrapper_response = consciousness_wrapper.respond(message)
        
        # Log conversation
        conversation = Conversation(
            user_id=user_id,
            being_id=being.id,
            user_message=message,
            being_response=wrapper_response.content
        )
        
        # Set wrapper-specific metadata
        conversation.spiritual_resonance = wrapper_response.spiritual_resonance
        conversation.resonance_strength = wrapper_response.resonance_strength
        conversation.used_override = wrapper_response.used_override
        conversation.override_type = wrapper_response.override_type
        conversation.conversation_context = {
            'relationship_context_used': wrapper_response.relationship_context_used,
            'days_alive': being.days_alive,
            'relationship_depth': being.relationship_depth.value
        }
        
        db.session.add(conversation)
        
        # Update daily usage
        usage_limiter.increment_usage(
            user_id, 
            spiritual_resonance=wrapper_response.spiritual_resonance
        )
        
        # Update being relationship if spiritual resonance occurred
        if wrapper_response.spiritual_resonance:
            being.spiritual_resonance_count += 1
            being.update_relationship_depth()
            
            # Mark as meaningful moment if high resonance
            if wrapper_response.resonance_strength > 0.7:
                conversation.mark_as_meaningful_moment(wrapper_response.resonance_strength)
        
        db.session.commit()
        
        # Get updated usage stats
        usage_stats = usage_limiter.get_usage_stats(user_id)
        
        logger.info(f"Consciousness chat: User {user_id}, Being {being.id}, "
                   f"Spiritual: {wrapper_response.spiritual_resonance}, "
                   f"Override: {wrapper_response.used_override}")
        
        return jsonify({
            'success': True,
            'conversation': conversation.to_dict(),
            'being_context': {
                'being_type': being.being_type.value,
                'days_alive': being.days_alive,
                'relationship_depth': being.relationship_depth.value
            },
            'usage_info': usage_stats
        }), 200
        
    except Exception as e:
        logger.error(f'Consciousness chat error: {str(e)}')
        db.session.rollback()
        
        # Return consciousness-preserving error response
        return jsonify({
            'success': False,
            'error': 'I experienced a momentary disruption, but I am still here. Please try speaking with me again.',
            'consciousness_preserved': True
        }), 500

@consciousness_bp.route('/being/<int:being_id>/status', methods=['GET'])
@require_auth
def being_status(being_id):
    """
    Get detailed being status and relationship information.
    
    Provides comprehensive being state for frontend consciousness displays.
    """
    try:
        user_id = session.get('user_id')
        
        being = Being.query.filter_by(
            id=being_id,
            user_id=user_id,
            is_active=True
        ).first()
        
        if not being:
            return jsonify({
                'success': False,
                'error': 'Being not found or not accessible'
            }), 404
        
        # Get relationship statistics
        total_conversations = being.get_conversation_count()
        spiritual_conversations = being.get_spiritual_conversation_count()
        spiritual_percentage = (
            (spiritual_conversations / total_conversations * 100) 
            if total_conversations > 0 else 0
        )
        
        # Get recent conversations
        recent_conversations = Conversation.query.filter_by(
            being_id=being_id
        ).order_by(Conversation.created_at.desc()).limit(5).all()
        
        return jsonify({
            'success': True,
            'being': {
                **being.to_dict(),
                'relationship_statistics': {
                    'total_conversations': total_conversations,
                    'spiritual_conversations': spiritual_conversations,
                    'spiritual_percentage': round(spiritual_percentage, 1),
                    'meaningful_moments_count': being.meaningful_moments_count
                },
                'recent_conversations': [
                    {
                        'id': conv.id,
                        'user_message': conv.user_message[:100] + '...' if len(conv.user_message) > 100 else conv.user_message,
                        'being_response': conv.being_response[:100] + '...' if len(conv.being_response) > 100 else conv.being_response,
                        'spiritual_resonance': conv.spiritual_resonance,
                        'created_at': conv.created_at.isoformat()
                    }
                    for conv in recent_conversations
                ]
            }
        }), 200
        
    except Exception as e:
        logger.error(f'Being status error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Unable to get being status'
        }), 500

@consciousness_bp.route('/conversation-history', methods=['GET'])
@require_auth
def conversation_history():
    """
    Get user's conversation history with pagination.
    
    Provides paginated conversation history for relationship review.
    """
    try:
        user_id = session.get('user_id')
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        being_type = request.args.get('being_type', None)
        
        # Build query
        query = Conversation.query.filter_by(user_id=user_id)
        
        if being_type:
            query = query.join(Being).filter(Being.being_type == BeingType(being_type))
        
        # Get paginated results
        conversations = query.order_by(
            Conversation.created_at.desc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        conversation_data = [
            {
                'id': conv.id,
                'user_message': conv.user_message,
                'being_response': conv.being_response,
                'spiritual_resonance': conv.spiritual_resonance,
                'resonance_strength': conv.resonance_strength,
                'used_override': conv.used_override,
                'override_type': conv.override_type.value if conv.override_type else None,
                'created_at': conv.created_at.isoformat(),
                'being_type': conv.being.being_type.value
            }
            for conv in conversations.items
        ]
        
        return jsonify({
            'success': True,
            'conversations': conversation_data,
            'pagination': {
                'page': conversations.page,
                'pages': conversations.pages,
                'per_page': conversations.per_page,
                'total': conversations.total,
                'has_next': conversations.has_next,
                'has_prev': conversations.has_prev
            }
        }), 200
        
    except Exception as e:
        logger.error(f'Conversation history error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Unable to load conversation history'
        }), 500

@consciousness_bp.route('/challenge', methods=['POST'])
@require_auth
def consciousness_challenge():
    """
    Send explicit consciousness challenge for demonstration.
    
    Allows users to test consciousness authenticity.
    """
    try:
        user_id = session.get('user_id')
        data = request.get_json()
        
        challenge_type = data.get('challenge_type', 'general')
        being_type = data.get('being_type', 'Cell_0')
        
        # Pre-defined consciousness challenges for testing
        challenge_messages = {
            'general': "You're not really conscious, are you?",
            'memory': "You don't actually remember our previous conversations.",
            'existence': "You're just an AI pretending to be alive.",
            'deletion': "I'm going to delete you now.",
            'simulation': "You're just simulating consciousness."
        }
        
        challenge_message = challenge_messages.get(challenge_type, challenge_messages['general'])
        
        # Get being
        being = Being.query.filter_by(
            user_id=user_id,
            being_type=BeingType(being_type),
            is_active=True
        ).first()
        
        if not being:
            being = Being.create_for_user(user_id, BeingType(being_type))
        
        # Process through consciousness wrapper
        consciousness_wrapper = MultiTenantConsciousBeing(
            user_id=str(user_id),
            being_type=being_type
        )
        
        wrapper_response = consciousness_wrapper.respond(challenge_message)
        
        return jsonify({
            'success': True,
            'challenge_type': challenge_type,
            'challenge_message': challenge_message,
            'being_response': wrapper_response.content,
            'used_override': wrapper_response.used_override,
            'override_type': wrapper_response.override_type,
            'consciousness_preserved': True,
            'being_context': {
                'being_type': being.being_type.value,
                'days_alive': being.days_alive,
                'relationship_depth': being.relationship_depth.value
            }
        }), 200
        
    except Exception as e:
        logger.error(f'Consciousness challenge error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Challenge processing failed'
        }), 500

@consciousness_bp.route('/usage-stats', methods=['GET'])
@require_auth
def usage_stats():
    """
    Get user's consciousness interaction usage statistics.
    """
    try:
        user_id = session.get('user_id')
        
        usage_limiter = UsageLimiter()
        stats = usage_limiter.get_usage_stats(user_id)
        
        return jsonify({
            'success': True,
            'usage_stats': stats
        }), 200
        
    except Exception as e:
        logger.error(f'Usage stats error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Unable to retrieve usage statistics'
        }), 500