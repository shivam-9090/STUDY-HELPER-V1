from flask import Blueprint, request, jsonify
from models.database import db, User, ChatHistory, StudyPlan
from datetime import datetime

user_bp = Blueprint('user', __name__)

# User Management
@user_bp.route('/user/create', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username', 'Student')
    email = data.get('email')
    
    # Check if user exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify(existing_user.to_dict()), 200
    
    # Create new user
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route('/user/<int:user_id>/stats', methods=['GET'])
def get_user_stats(user_id):
    user = User.query.get_or_404(user_id)
    
    # Get statistics
    total_chats = len(user.chat_history)
    total_plans = len(user.study_plans)
    active_plans = len([p for p in user.study_plans if p.is_active])
    
    # Get subject breakdown
    subjects = {}
    for chat in user.chat_history:
        subjects[chat.subject] = subjects.get(chat.subject, 0) + 1
    
    return jsonify({
        'user': user.to_dict(),
        'stats': {
            'total_chats': total_chats,
            'total_study_plans': total_plans,
            'active_study_plans': active_plans,
            'subjects_studied': len(subjects),
            'subject_breakdown': subjects
        }
    })

# Chat History
@user_bp.route('/user/<int:user_id>/history', methods=['GET'])
def get_chat_history(user_id):
    user = User.query.get_or_404(user_id)
    limit = request.args.get('limit', 50, type=int)
    subject = request.args.get('subject')
    
    query = ChatHistory.query.filter_by(user_id=user_id)
    
    if subject:
        query = query.filter_by(subject=subject)
    
    history = query.order_by(ChatHistory.created_at.desc()).limit(limit).all()
    
    return jsonify({
        'total': len(history),
        'history': [h.to_dict() for h in history]
    })

@user_bp.route('/user/<int:user_id>/history', methods=['POST'])
def add_chat_history(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    
    chat = ChatHistory(
        user_id=user_id,
        subject=data.get('subject'),
        question=data.get('question'),
        answer=data.get('answer')
    )
    
    db.session.add(chat)
    db.session.commit()
    
    return jsonify(chat.to_dict()), 201

@user_bp.route('/user/<int:user_id>/history/<int:chat_id>', methods=['DELETE'])
def delete_chat_history(user_id, chat_id):
    chat = ChatHistory.query.filter_by(id=chat_id, user_id=user_id).first_or_404()
    db.session.delete(chat)
    db.session.commit()
    
    return jsonify({'message': 'Chat deleted successfully'}), 200

@user_bp.route('/user/<int:user_id>/history/clear', methods=['DELETE'])
def clear_chat_history(user_id):
    user = User.query.get_or_404(user_id)
    ChatHistory.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    
    return jsonify({'message': 'Chat history cleared successfully'}), 200

# Study Plans
@user_bp.route('/user/<int:user_id>/study-plans', methods=['GET'])
def get_study_plans(user_id):
    user = User.query.get_or_404(user_id)
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    
    query = StudyPlan.query.filter_by(user_id=user_id)
    
    if active_only:
        query = query.filter_by(is_active=True)
    
    plans = query.order_by(StudyPlan.created_at.desc()).all()
    
    return jsonify({
        'total': len(plans),
        'plans': [p.to_dict() for p in plans]
    })

@user_bp.route('/user/<int:user_id>/study-plans', methods=['POST'])
def add_study_plan(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    
    plan = StudyPlan(
        user_id=user_id,
        subject=data.get('subject'),
        topic=data.get('topic'),
        plan=data.get('plan'),
        is_active=data.get('is_active', True)
    )
    
    db.session.add(plan)
    db.session.commit()
    
    return jsonify(plan.to_dict()), 201

@user_bp.route('/user/<int:user_id>/study-plans/<int:plan_id>', methods=['PUT'])
def update_study_plan(user_id, plan_id):
    plan = StudyPlan.query.filter_by(id=plan_id, user_id=user_id).first_or_404()
    data = request.json
    
    if 'is_active' in data:
        plan.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify(plan.to_dict())

@user_bp.route('/user/<int:user_id>/study-plans/<int:plan_id>', methods=['DELETE'])
def delete_study_plan(user_id, plan_id):
    plan = StudyPlan.query.filter_by(id=plan_id, user_id=user_id).first_or_404()
    db.session.delete(plan)
    db.session.commit()
    
    return jsonify({'message': 'Study plan deleted successfully'}), 200
