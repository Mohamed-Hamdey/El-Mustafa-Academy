from flask import Blueprint, request, jsonify, render_template, url_for
from flask_login import login_required, current_user
from app.models import Video, Course, db

bp = Blueprint('videos', __name__)

@bp.route('/videos/page', methods=['GET'])
@login_required
def video_page():
    return student_video_page()

@bp.route('/videos', methods=['GET'])
@login_required
def get_videos():
    course_id = request.args.get('course_id', type=int)

    if course_id:
        videos = Video.query.filter_by(course_id=course_id).all()
    else:
        videos = [v for e in current_user.enrollments for v in e.course.videos]

    return jsonify([{
        'id': v.id,
        'course_id': v.course_id,
        'title': v.title,
        'description': v.description,
        'url': v.url,
        'upload_date': v.upload_date.isoformat(),
        'video_page': url_for('videos.get_video', video_id=v.id)
    } for v in videos]), 200

@bp.route('/videos/create', methods=['POST'])
@login_required
def create_video():
    data = request.get_json()
    course = Course.query.get_or_404(data['course_id'])
    
    video = Video(
        course_id=data['course_id'],
        title=data['title'],
        description=data['description'],
        url=data['url']
    )
    db.session.add(video)
    db.session.commit()
    return jsonify({'message': 'Video uploaded successfully', 'id': video.id}), 201

@bp.route('/videos/<int:video_id>', methods=['GET'])
@login_required
def get_video(video_id):
    video = Video.query.get_or_404(video_id)
    if video.views >= video.max_views:
        return render_template('error/403.html')

    video.views += 1
    db.session.commit()

    return jsonify({
        'id': video.id,
        'course_id': video.course_id,
        'title': video.title,
        'description': video.description,
        'url': video.url,
        'upload_date': video.upload_date.isoformat()
    }), 200

@bp.route('/videos/<int:video_id>/update', methods=['PUT'])
@login_required
def update_video(video_id):
    video = Video.query.get_or_404(video_id)

    data = request.get_json()
    video.title = data.get('title', video.title)
    video.description = data.get('description', video.description)
    video.url = data.get('url', video.url)

    db.session.commit()
    return jsonify({'message': 'Video updated successfully'}), 200

@bp.route('/videos/<int:video_id>/delete', methods=['DELETE'])
@login_required
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)

    db.session.delete(video)
    db.session.commit()
    return jsonify({'message': 'Video deleted successfully'}), 200

@bp.route('/teacher/dashboard', methods=['GET'])
@login_required
def teacher_dashboard():
    courses = Course.query.filter_by(teacher_id=current_user.id).all()
    return render_template('dashboard.html', courses=courses)

@bp.route('/student/videos', methods=['GET'])
@login_required
def student_video_page():
    videos = [v for e in current_user.enrollments for v in e.course.videos]
    return render_template('External_pages/video.html', videos=videos)
