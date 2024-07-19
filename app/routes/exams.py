from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app.models import Exam, db
from datetime import datetime

bp = Blueprint('exams', __name__)

@bp.route('/exams')
@login_required
def exams_page():
    return render_template('External_pages/Exam.html')

@bp.route('/api/exams', methods=['GET'])
@login_required
def get_exams():
    exams = Exam.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'date': e.date.isoformat()
    } for e in exams]), 200

@bp.route('/api/exams', methods=['POST'])
@login_required
def create_exam():
    data = request.get_json()
    exam = Exam(
        title=data['title'],
        description=data['description'],
        date=datetime.fromisoformat(data['date']),
        user_id=current_user.id
    )
    db.session.add(exam)
    db.session.commit()
    return jsonify({'message': 'Exam created successfully', 'id': exam.id}), 201

@bp.route('/api/exams/<int:exam_id>', methods=['GET'])
@login_required
def get_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    if exam.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized access'}), 403
    return jsonify({
        'id': exam.id,
        'title': exam.title,
        'description': exam.description,
        'date': exam.date.isoformat()
    }), 200

@bp.route('/api/exams/<int:exam_id>', methods=['PUT'])
@login_required
def update_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    if exam.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized access'}), 403

    data = request.get_json()
    exam.title = data.get('title', exam.title)
    exam.description = data.get('description', exam.description)
    exam.date = datetime.fromisoformat(data.get('date', exam.date.isoformat()))

    db.session.commit()
    return jsonify({'message': 'Exam updated successfully'}), 200

@bp.route('/api/exams/<int:exam_id>', methods=['DELETE'])
@login_required
def delete_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    if exam.user_id != current_user.id:
        return jsonify({'message': 'Unauthorized access'}), 403

    db.session.delete(exam)
    db.session.commit()
    return jsonify({'message': 'Exam deleted successfully'}), 200

@bp.errorhandler(404)
def not_found_error(error):
    return render_template('error/404.html'), 404

@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error/500.html'), 500
