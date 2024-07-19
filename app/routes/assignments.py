from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app.models import Assignment, db
from datetime import datetime

bp = Blueprint('assignments', __name__)

@bp.route('/assignments', methods=['GET'])
@login_required
def get_assignments():
    assignments = Assignment.query.filter_by(stage=current_user.stage).all()  # Filter by user's stage
    return jsonify([{
        'id': a.id,
        'title': a.title,
        'description': a.description,
        'upload_date': a.upload_date.isoformat(),
        'subject': a.subject,
        'file_path': a.file_path
    } for a in assignments]), 200

@bp.route('/assignments', methods=['POST'])
@login_required
def create_assignment():
    data = request.get_json()
    assignment = Assignment(
        title=data['title'],
        description=data['description'],
        subject=data['subject'],
        stage=data['stage'],  # Added stage field
        file_path=data['file_path'],
        user_id=current_user.id
    )
    db.session.add(assignment)
    db.session.commit()
    return jsonify({'message': 'Assignment created successfully', 'id': assignment.id}), 201

@bp.route('/assignments/<int:assignment_id>', methods=['GET'])
@login_required
def get_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    if assignment.stage != current_user.stage:
        return render_template('error/403.html')  # User should not access assignments not in their stage

    return jsonify({
        'id': assignment.id,
        'title': assignment.title,
        'description': assignment.description,
        'upload_date': assignment.upload_date.isoformat(),
        'subject': assignment.subject,
        'file_path': assignment.file_path
    }), 200

@bp.route('/assignments/<int:assignment_id>', methods=['PUT'])
@login_required
def update_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)

    data = request.get_json()
    assignment.title = data.get('title', assignment.title)
    assignment.description = data.get('description', assignment.description)
    assignment.upload_date = datetime.fromisoformat(data.get('upload_date', assignment.upload_date.isoformat()))
    assignment.subject = data.get('subject', assignment.subject)
    assignment.file_path = data.get('file_path', assignment.file_path)
    assignment.stage = data.get('stage', assignment.stage)  # Added stage field

    db.session.commit()
    return jsonify({'message': 'Assignment updated successfully'}), 200

@bp.route('/assignments/<int:assignment_id>', methods=['DELETE'])
@login_required
def delete_assignment(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    db.session.delete(assignment)
    db.session.co
