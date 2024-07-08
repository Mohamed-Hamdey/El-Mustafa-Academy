from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Course, Enrollment, db

bp = Blueprint('courses', __name__)

@bp.route('/courses', methods=['GET'])
@login_required
def get_courses():
    if current_user.user_type == 'Teacher':
        courses = Course.query.filter_by(teacher_id=current_user.id).all()
    else:
        enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
        courses = [enrollment.course for enrollment in enrollments]
    
    return jsonify([{
        'id': course.id,
        'name': course.name,
        'teacher_id': course.teacher_id
    } for course in courses]), 200

@bp.route('/courses', methods=['POST'])
@login_required
def create_course():
    if current_user.user_type != 'Teacher':
        return jsonify({'message': 'Only teachers can create courses'}), 403
    
    data = request.get_json()
    course = Course(name=data['name'], teacher_id=current_user.id)
    db.session.add(course)
    db.session.commit()
    return jsonify({'message': 'Course created successfully', 'id': course.id}), 201

@bp.route('/courses/<int:course_id>', methods=['GET'])
@login_required
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return jsonify({
        'id': course.id,
        'name': course.name,
        'teacher_id': course.teacher_id
    }), 200

@bp.route('/courses/<int:course_id>/enroll', methods=['POST'])
@login_required
def enroll_course(course_id):
    if current_user.user_type != 'Student':
        return jsonify({'message': 'Only students can enroll in courses'}), 403
    
    course = Course.query.get_or_404(course_id)
    if Enrollment.query.filter_by(student_id=current_user.id, course_id=course_id).first():
        return jsonify({'message': 'Already enrolled in this course'}), 400
    
    enrollment = Enrollment(student_id=current_user.id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({'message': 'Enrolled successfully'}), 201