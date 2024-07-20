from flask import Blueprint, request, jsonify, render_template, current_app
from flask_login import login_required, current_user
from app.models import Course, db
from werkzeug.utils import secure_filename
import os
from datetime import datetime

bp = Blueprint('courses', __name__)

@bp.route('/courses', methods=['GET'])
@login_required
def get_courses():
    courses = Course.query.filter_by(stage=current_user.stage).all()
    return render_template('External_pages/courses.html', courses=courses)

@bp.route('/courses', methods=['POST'])
@login_required
def add_course():
    title = request.form.get('title')
    description = request.form.get('description')
    subject = request.form.get('subject')
    stage = request.form.get('stage')
    file = request.files.get('file')

    if not all([title, description, subject, stage, file]):
        return jsonify({'message': 'Missing data'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    course = Course(
        title=title,
        description=description,
        subject=subject,
        stage=stage,
        file_path=file_path,
        user_id=current_user.id
    )
    db.session.add(course)
    db.session.commit()
    return jsonify({'message': 'Course uploaded successfully', 'id': course.id}), 201

@bp.route('/courses/<int:course_id>', methods=['GET'])
@login_required
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('courses/detail.html', course=course)

@bp.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
def update_course(course_id):
    course = Course.query.get_or_404(course_id)

    if request.method == 'POST':
        data = request.form
        course.title = data.get('title', course.title)
        course.description = data.get('description', course.description)
        course.subject = data.get('subject', course.subject)
        course.stage = data.get('stage', course.stage)

        db.session.commit()
        return jsonify({'message': 'Course updated successfully'}), 200
    
    return render_template('courses/edit.html', course=course)

@bp.route('/courses/<int:course_id>/delete', methods=['POST'])
@login_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course deleted successfully'}), 200

@bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
