from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Grade, Course, db
from datetime import datetime

bp = Blueprint('grades', __name__)

@bp.route('/grades', methods=['GET'])
@login_required
def get_grades():
    course_id = request.args.get('course_id', type=int)
    if course_id:
        grades = Grade.query.filter_by(course_id=course_id).all()
    else:
        if current_user.user_type == 'Teacher':
            courses = Course.query.filter_by(teacher_id=current_user.id).all()
            grades = [g for c in courses for g in c.grades]
        else:
            grades = current_user.grades

    return render_template('grades/list.html', grades=grades)

@bp.route('/first', methods=['GET'])
@login_required
def get_first_grade():
    grades = Grade.query.filter_by(student_id=current_user.id, grade_type='first').all()
    return render_template('grades/first-Login.html', grades=grades)

@bp.route('/second', methods=['GET'])
@login_required
def get_second_grade():
    grades = Grade.query.filter_by(student_id=current_user.id, grade_type='second').all()
    return render_template('grades/second-Login.html', grades=grades)

@bp.route('/third', methods=['GET'])
@login_required
def get_third_grade():
    grades = Grade.query.filter_by(student_id=current_user.id, grade_type='third').all()
    return render_template('grades/third-Login.html', grades=grades)

@bp.route('/grades', methods=['POST'])
@login_required
def create_grade():
    if current_user.user_type != 'Teacher':
        return render_template('errors/403.html'), 403

    data = request.form
    course = Course.query.get_or_404(data['course_id'])
    if course.teacher_id != current_user.id:
        return render_template('errors/403.html'), 403

    grade = Grade(
        course_id=data['course_id'],
        student_id=data['student_id'],
        grade_value=data['grade_value'],
        grade_type=data['grade_type']
    )
    db.session.add(grade)
    db.session.commit()
    return render_template('grades/create_success.html', grade=grade)

@bp.route('/grades/<int:grade_id>', methods=['GET'])
@login_required
def get_grade(grade_id):
    grade = Grade.query.get_or_404(grade_id)
    return render_template('grades/detail.html', grade=grade)

@bp.route('/grades/<int:grade_id>/edit', methods=['GET', 'POST'])
@login_required
def update_grade(grade_id):
    if current_user.user_type != 'Teacher':
        return render_template('errors/403.html'), 403

    grade = Grade.query.get_or_404(grade_id)
    if grade.course.teacher_id != current_user.id:
        return render_template('errors/403.html'), 403

    if request.method == 'POST':
        data = request.form
        grade.grade_value = data.get('grade_value', grade.grade_value)
        grade.grade_type = data.get('grade_type', grade.grade_type)
        db.session.commit()
        return render_template('grades/update_success.html', grade=grade)
    
    return render_template('grades/edit.html', grade=grade)

@bp.route('/grades/<int:grade_id>/delete', methods=['POST'])
@login_required
def delete_grade(grade_id):
    if current_user.user_type != 'Teacher':
        return render_template('errors/403.html'), 403

    grade = Grade.query.get_or_404(grade_id)
    if grade.course.teacher_id != current_user.id:
        return render_template('errors/403.html'), 403

    db.session.delete(grade)
    db.session.commit()
    return render_template('grades/delete_success.html')

@bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
