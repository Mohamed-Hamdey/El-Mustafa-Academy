from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Exam, Course, db
from datetime import datetime

bp = Blueprint('exams', __name__)

@bp.route('/exams', methods=['GET'])
@login_required
def get_exams():
    course_id = request.args.get('course_id', type=int)
    if course_id:
        exams = Exam.query.filter_by(course_id=course_id).all()
    else:
        if current_user.user_type == 'Teacher':
            courses = Course.query.filter_by(teacher_id=current_user.id).all()
            exams = [e for c in courses for e in c.exams]
        else:
            exams = [e for enrollment in current_user.enrollments for e in enrollment.course.exams]

    return jsonify([{
        'id': e.id,
        'course_id': e.course_id,
        'title': e.title,
        'description': e.description,
        'exam_date': e.exam_date.isoformat(),
        'duration': e.duration
    } for e in exams]), 200

@bp.route('/exams', methods=['POST'])
@login_required
def create_exam():
    if current_user.user_type != 'Teacher':
        return jsonify({'message': 'Only teachers can create exams'}), 403

    data = request.get_json()
    course = Course.query.get_or_404(data['course_id'])
    if course.teacher_id != current_user.id:
        return jsonify({'message': 'You can only create exams for your own courses'}), 403

    exam = Exam(
        course_id=data['course_id'],
        title=data['title'],
        description=data['description'],
        exam_date=datetime.fromisoformat(data['exam_date']),
        duration=data['duration']
    )
    db.session.add(exam)
    db.session.commit()
    return jsonify({'message': 'Exam created successfully', 'id': exam.id}), 201

@bp.route('/exams/<int:exam_id>', methods=['GET'])
@login_required
def get_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    return jsonify({
        'id': exam.id,
        'course_id': exam.course_id,
        'title': exam.title,
        'description': exam.description,
        'exam_date': exam.exam_date.isoformat(),
        'duration': exam.duration
    }), 200

@bp.route('/exams/<int:exam_id>', methods=['PUT'])
@login_required
def update_exam(exam_id):
    if current_user.user_type != 'Teacher':
        return jsonify({'message': 'Only teachers can update exams'}), 403

    exam = Exam.query.get_or_404(exam_id)
    if exam.course.teacher_id != current_user.id:
        return jsonify({'message': 'You can only update your own exams'}), 403

    data = request.get_json()
    exam.title = data.get('title', exam.title)
    exam.description = data.get('description', exam.description)
    exam.exam_date = datetime.fromisoformat(data.get('exam_date', exam.exam_date.isoformat()))
    exam.duration = data.get('duration', exam.duration)

    db.session.commit()
    return jsonify({'message': 'Exam updated successfully'}), 200

@bp.route('/exams/<int:exam_id>', methods=['DELETE'])
@login_required
def delete_exam(exam_id):
    if current_user.user_type != 'Teacher':
        return jsonify({'message': 'Only teachers can delete exams'}), 403

    exam = Exam.query.get_or_404(exam_id)
    if exam.course.teacher_id != current_user.id:
        return jsonify({'message': 'You can only delete your own exams'}), 403

    db.session.delete(exam)
    db.session.commit()
    return jsonify({'message': 'Exam deleted successfully'}), 200