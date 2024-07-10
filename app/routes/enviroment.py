from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import EnvironmentTopic, Course, db

bp = Blueprint('environment', __name__)

@bp.route('/environment-topics', methods=['GET'])
@login_required
def get_environment_topics():
    course_id = request.args.get('course_id', type=int)
    if course_id:
        topics = EnvironmentTopic.query.filter_by(course_id=course_id).all()
    else:
        if current_user.user_type == 'Teacher':
            courses = Course.query.filter_by(teacher_id=current_user.id).all()
            topics = [t for c in courses for t in c.environment_topics]
        else:
            topics = [t for e in current_user.enrollments for t in e.course.environment_topics]

    return jsonify([{
        'id': t.id,
        'course_id': t.course_id,
        'title': t.title,
        'content': t.content
    } for t in topics]), 200

@bp.route('/environment-topics', methods=['POST'])
@login_required
def create_environment_topic():
    if current_user.user_type != 'Teacher':
        return jsonify({'message': 'Only teachers can create environment topics'}), 403

    data = request.get_json()
    if not data or 'course_id' not in data or 'title' not in data or 'content' not in data:
        return jsonify({'message': 'Missing required data'}), 400

    course = Course.query.get_or_404(data['course_id'])
    if course.teacher_id != current_user.id:
        return jsonify({'message': 'You can only create topics for your own courses'}), 403

    topic = EnvironmentTopic(
        course_id=data['course_id'],
        title=data['title'],
        content=data['content']
    )
    db.session.add(topic)
    db.session.commit()
    return jsonify({'message': 'Environment topic created successfully', 'id': topic.id}), 201

@bp.route('/environment-topics/<int:topic_id>', methods=['GET'])
@login_required
def get_environment_topic(topic_id):
    topic = EnvironmentTopic.query.get_or_404(topic_id)
    return jsonify({
        'id': topic.id,
        'course_id': topic.course_id,
        'title': topic.title,
        'content': topic.content
    }), 200

@bp.route('/environment-topics/<int:topic_id>', methods=['PUT'])
@login_required
def update_environment_topic(topic_id):
    if current_user.user_type != 'Teacher':
        return jsonify({'message': 'Only teachers can update environment topics'}), 403

    topic = EnvironmentTopic.query.get_or_404(topic_id)
    if topic.course.teacher_id != current_user.id:
        return jsonify({'message': 'You can only update your own topics'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    topic.title = data.get('title', topic.title)
    topic.content = data.get('content', topic.content)

    db.session.commit()
    return jsonify({'message': 'Environment topic updated successfully'}), 200

@bp.route('/environment-topics/<int:topic_id>', methods=['DELETE'])
@login_required
def delete_environment_topic(topic_id):
    if current_user.user_type != 'Teacher':
        return jsonify({'message': 'Only teachers can delete environment topics'}), 403

    topic = EnvironmentTopic.query.get_or_404(topic_id)
    if topic.course.teacher_id != current_user.id:
        return jsonify({'message': 'You can only delete your own topics'}), 403

    db.session.delete(topic)
    db.session.commit()
    return jsonify({'message': 'Environment topic deleted successfully'}), 200

@bp.errorhandler(404)
def not_found_error(error):
    return jsonify({'message': 'Resource not found'}), 404

@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'message': 'An internal error occurred'}), 500