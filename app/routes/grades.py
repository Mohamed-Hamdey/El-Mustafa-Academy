from flask import Blueprint, request, render_template
from flask_login import login_required, current_user
from app.models import Course, db

bp = Blueprint('grades', __name__)

@bp.route('/grades', methods=['GET'])
@login_required
def get_grades():
    grades = Course.query.all()
    return render_template('grades/list.html', grades=grades)

@bp.route('/grades', methods=['POST'])
@login_required
def add_course():
    data = request.form
    grade = Course(
        student_id=data['student_id'],
        course_id=data['course_id'],
        grade_value=data['grade_value'],
        grade_type=data['grade_type']
    )
    db.session.add(grade)
    db.session.commit()
    return render_template('grades/create_success.html', grade=grade)

@bp.route('/grades/<int:grade_id>', methods=['GET'])
@login_required
def get_grade(grade_id):
    grade = Course.query.get_or_404(grade_id)
    return render_template('grades/detail.html', grade=grade)

@bp.route('/grades/<int:grade_id>/edit', methods=['GET', 'POST'])
@login_required
def update_grade(grade_id):
    grade = Course.query.get_or_404(grade_id)

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
    grade = Course.query.get_or_404(grade_id)
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
