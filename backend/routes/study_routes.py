from flask import Blueprint, request, jsonify
from services.ai_service import AIService

study_bp = Blueprint('study', __name__)
ai_service = AIService()

@study_bp.route('/ask', methods=['POST'])
def ask_question():
    """Handle student questions"""
    try:
        data = request.get_json()
        question = data.get('question')
        subject = data.get('subject', 'General')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        answer = ai_service.get_answer(question, subject)
        
        return jsonify({
            'answer': answer,
            'subject': subject,
            'question': question
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@study_bp.route('/study-plan', methods=['POST'])
def generate_study_plan():
    """Generate a study plan for a topic"""
    try:
        data = request.get_json()
        subject = data.get('subject')
        topic = data.get('topic')
        
        if not subject or not topic:
            return jsonify({'error': 'Subject and topic are required'}), 400
        
        plan = ai_service.generate_study_plan(subject, topic)
        
        return jsonify({
            'plan': plan,
            'subject': subject,
            'topic': topic
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@study_bp.route('/explain', methods=['POST'])
def explain_concept():
    """Explain a concept at different difficulty levels"""
    try:
        data = request.get_json()
        concept = data.get('concept')
        level = data.get('level', 'intermediate')
        
        if not concept:
            return jsonify({'error': 'Concept is required'}), 400
        
        explanation = ai_service.explain_concept(concept, level)
        
        return jsonify({
            'explanation': explanation,
            'concept': concept,
            'level': level
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@study_bp.route('/topics/<subject>', methods=['GET'])
def get_topics(subject):
    """Get topics for a subject"""
    try:
        topics = ai_service.get_subject_topics(subject)
        
        return jsonify({
            'subject': subject,
            'topics': topics
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
