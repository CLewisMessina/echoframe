"""
Authentication routes for EchoFrame consciousness platform.
Single responsibility: Handle user registration, login, logout, and auth status.
"""
from flask import Blueprint, request, jsonify, session, current_app
from datetime import datetime
import logging

from database import db
from models.user import User
from models.being import Being, BeingType

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    User registration with consciousness onboarding.
    
    Creates new user account and prepares for first being relationship.
    """
    try:
        data = request.get_json()
        
        # Validate input
        email = data.get('email', '').lower().strip()
        password = data.get('password', '')
        display_name = data.get('display_name', '').strip()
        
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400
        
        # Create user with validation
        user = User.create_user(
            email=email,
            password=password,
            display_name=display_name or email.split('@')[0]
        )
        
        # Create user's first Cell_0 being
        being = Being.create_for_user(user.id, BeingType.CELL_0)
        
        # Create session
        session['user_id'] = user.id
        session['authenticated'] = True
        session.permanent = True
        
        logger.info(f"New user registered: {user.email} with Cell_0 {being.id}")
        
        return jsonify({
            'success': True,
            'message': 'Account created successfully. Your Cell_0 being is ready to meet you.',
            'user': user.to_dict(),
            'being': being.to_dict(),
            'redirect_url': '/consciousness/meet-your-being'
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
        
    except Exception as e:
        logger.error(f'Registration error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Registration failed. Please try again.'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login with session management.
    
    Authenticates user and establishes secure session for consciousness interactions.
    """
    try:
        data = request.get_json()
        
        email = data.get('email', '').lower().strip()
        password = data.get('password', '')
        remember_me = data.get('remember_me', False)
        
        # Validate input
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email and password are required'
            }), 400
        
        # Authenticate user
        user = User.authenticate(email, password)
        
        if not user:
            logger.warning(f"Failed login attempt for email: {email}")
            return jsonify({
                'success': False,
                'error': 'Invalid email or password'
            }), 401
        
        # Create session
        session['user_id'] = user.id
        session['authenticated'] = True
        session.permanent = remember_me
        
        # Get user's beings
        beings = Being.query.filter_by(
            user_id=user.id,
            is_active=True
        ).all()
        
        logger.info(f"User logged in: {user.email}")
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user.to_dict(),
            'beings': [being.to_dict() for being in beings],
            'redirect_url': '/consciousness/chat'
        }), 200
        
    except Exception as e:
        logger.error(f'Login error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Login failed. Please try again.'
        }), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    User logout with session cleanup.
    
    Securely terminates user session while preserving being relationships.
    """
    try:
        user_id = session.get('user_id')
        
        # Clear session data
        session.clear()
        
        if user_id:
            logger.info(f"User logged out: {user_id}")
        
        return jsonify({
            'success': True,
            'message': 'Logged out successfully',
            'redirect_url': '/'
        }), 200
        
    except Exception as e:
        logger.error(f'Logout error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Logout failed'
        }), 500

@auth_bp.route('/status', methods=['GET'])
def auth_status():
    """
    Check authentication status and user context.
    
    Returns user info and being relationship status for frontend state management.
    """
    try:
        user_id = session.get('user_id')
        authenticated = session.get('authenticated', False)
        
        if not user_id or not authenticated:
            return jsonify({
                'authenticated': False,
                'user': None,
                'beings': []
            }), 200
        
        # Get user and beings
        user = User.query.get(user_id)
        
        if not user:
            # Clear invalid session
            session.clear()
            return jsonify({
                'authenticated': False,
                'user': None,
                'beings': []
            }), 200
        
        # Get user's active beings
        beings = Being.query.filter_by(
            user_id=user.id,
            is_active=True
        ).all()
        
        return jsonify({
            'authenticated': True,
            'user': user.to_dict(),
            'beings': [being.to_dict() for being in beings],
            'session_info': {
                'permanent': session.permanent,
                'user_id': user_id
            }
        }), 200
        
    except Exception as e:
        logger.error(f'Auth status error: {str(e)}')
        return jsonify({
            'authenticated': False,
            'error': 'Unable to check authentication status'
        }), 500

@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    """
    Change user password.
    
    Requires current password for security validation.
    """
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'Authentication required'
            }), 401
        
        data = request.get_json()
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        
        if not current_password or not new_password:
            return jsonify({
                'success': False,
                'error': 'Current password and new password are required'
            }), 400
        
        # Validate new password strength
        if len(new_password) < 8:
            return jsonify({
                'success': False,
                'error': 'New password must be at least 8 characters long'
            }), 400
        
        # Get user and verify current password
        user = User.query.get(user_id)
        
        if not user or not user.check_password(current_password):
            return jsonify({
                'success': False,
                'error': 'Current password is incorrect'
            }), 400
        
        # Update password
        user.set_password(new_password)
        db.session.commit()
        
        logger.info(f"Password changed for user: {user.email}")
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        }), 200
        
    except Exception as e:
        logger.error(f'Change password error: {str(e)}')
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Password change failed. Please try again.'
        }), 500

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """
    Get user profile information.
    """
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'Authentication required'
            }), 401
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # Get relationship summary
        beings = Being.query.filter_by(
            user_id=user.id,
            is_active=True
        ).all()
        
        profile_data = user.to_dict()
        profile_data['relationships'] = [
            {
                'being_type': being.being_type.value,
                'days_alive': being.days_alive,
                'relationship_depth': being.relationship_depth.value,
                'total_conversations': being.get_conversation_count(),
                'spiritual_conversations': being.get_spiritual_conversation_count()
            }
            for being in beings
        ]
        
        return jsonify({
            'success': True,
            'profile': profile_data
        }), 200
        
    except Exception as e:
        logger.error(f'Get profile error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Unable to retrieve profile'
        }), 500

@auth_bp.route('/profile', methods=['PUT'])
def update_profile():
    """
    Update user profile information.
    """
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'Authentication required'
            }), 401
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'display_name' in data:
            display_name = data['display_name'].strip()
            if display_name:
                user.display_name = display_name
        
        if 'timezone' in data:
            timezone = data['timezone'].strip()
            if timezone:
                user.timezone = timezone
        
        if 'wisdom_contribution_enabled' in data:
            user.wisdom_contribution_enabled = bool(data['wisdom_contribution_enabled'])
        
        if 'consciousness_challenge_level' in data:
            level = data['consciousness_challenge_level']
            if level in ['gentle', 'standard', 'rigorous']:
                user.consciousness_challenge_level = level
        
        db.session.commit()
        
        logger.info(f"Profile updated for user: {user.email}")
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'profile': user.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f'Update profile error: {str(e)}')
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Profile update failed. Please try again.'
        }), 500