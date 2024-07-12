from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Assignment, Course, db
from datetime import datetime

bp = Blueprint('assignments', __name__)

@bp.route('/assignments', methods=['GET'])
@login_required
def get_assignments():
    course_id = request.args.get('course_id', type=int)
    if course_id:
        assignments = Assignment.query.filter_by(course_id=course_id).all()
    else:
        if current_user.user_type == 'Teacher':
            courses = Course.query.filter_by(teacher_id=current_user.id).all()
            assignments = [a for c in courses for a in c.assignments]
        else:
            assignments = [a for e in current_user.enrollments for a in e.course.assignments]

    return jsonify([{
        'id': a.id,
        'course_id': a.course_id,
        'title': a.title,
        'description': a.description,
        'due_date': a.due_date.isoformat(),
        'assignment_type': a.assignment_type
    } for a in assignments]), 200

@bp.route('/assignments', methods=['POST'])
@login_required
def create_assignment():
    if current_user.user_type != 'Teacher':
        return jsonify({'message': 'Only teachers can create assignments'}), 403

    data = request.get_json()
    course = Course.query.get_or_404(data['course_id'])
    if course.teacher_id != current_user.id:
        return jsonify({'message': 'You can only create assignments for your own courses'}), 403

    assignment = Assignment(
        course_id=data['course_id'],
        title=data['title'],
        description=data['description'],
        due_date=datetime.fromisoformat(data['due_date']),
        assignment_type=data['assignment_type']
    )
    db.session.add(assignment)
    db.session.commit()
    return jsonify({'message': 'Assignment created successfully', 'id': assignment.id}), 201
    
@bp.route('/assignments/<int:assignment_id>', methods=['GET'])
@login_required
def get_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    return jsonify({
        'id': assignment.id,
        'course_id': assignment.course_id,
        'title': assignment.title,
        'description': assignment.description,
        'due_date': assignment.due_date.isoformat(),
        'assignment_type': assignment.assignment_type
    }), 200

@bp.route('/assignments/<int:assignment_id>', methods=['PUT'])
@login_required
def update_assignment(assignment_id):
    if current_user.user_type != 'Teacher':
        return jsonify({'message': 'Only teachers can update assignments'}), 403

    assignment = Assignment.query.get_or_404(assignment_id)
    if assignment.course.teacher_id != current_user.id:
        return jsonify({'message': 'You can only update your own assignments'}), 403

    data = request.get_json()
    assignment.title = data.get('title', assignment.title)
    assignment.description = data.get('description', assignment.description)
    assignment.due_date = datetime.fromisoformat(data.get('due_date', assignment.due_date.isoformat()))
    assignment.assignment_type = data.get('assignment_type', assignment.assignment_type)

    db.session.commit()
    return jsonify({'message': 'Assignment updated successfully'}), 200

@bp.route('/assignments/<int:assignment_id>', methods=['DELETE'])
@login_required
def delete_assignment(assignment_id):
    if current_user.user_type != 'Teacher':
        return jsonify({'message': 'Only teachers can delete assignments'}), 403

    assignment = Assignment.query.get_or_404(assignment_id)
    if assignment.course.teacher_id != current_user.id:
        return jsonify({'message': 'You can only delete your own assignments'}), 403

    db.session.delete(assignment)
    db.session.commit()
    return jsonify({'message': 'Assignment deleted successfully'}), 200

@bp.errorhandler(404)
def not_found_error(error):
    return jsonify({'message': 'Resource not found'}), 404

@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'message': 'An internal error occurred'}), 500