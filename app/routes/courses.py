from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app.models import Course, db

bp = Blueprint('courses', __name__)

@bp.route('/courses', methods=['GET'])
@login_required
def get_courses():
    # Get all courses for display
    courses = Course.query.all()
    return jsonify([{
        'id': course.id,
        'name': course.name,
        'teacher_id': course.teacher_id
    } for course in courses]), 200

@bp.route('/courses/create', methods=['POST'])
@login_required
def create_course():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')  # Default to empty string if not provided
    teacher_id = current_user.id
    
    # Assuming you have a Course model
    new_course = Course(name=name, description=description, teacher_id=teacher_id)
    db.session.add(new_course)
    db.session.commit()

    return jsonify({"message": "Course added successfully!"}), 201

@bp.route('/courses/page', methods=['GET'])
@login_required
def course_page():
    courses = Course.query.all()
    return render_template('External_pages/courses.html' ,courses=courses )


