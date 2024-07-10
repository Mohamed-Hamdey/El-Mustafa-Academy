from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Video, Course, db
from datetime import datetime

bp = Blueprint('videos', __name__)

@bp.route('/videos', methods=['GET'])
@login_required
def get_videos():
    course_id = request.args.get('course_id', type=int)
    if course_id:
        videos = Video.query.filter_by(course_id=course_id).all()
    else:
        if current_user.user_type == 'Teacher':
            courses = Course.query.filter_by(teacher_id=current_user.id).all()
            videos = [v for c in courses for v in c.videos]
        else:
            videos = [v for e in current_user.enrollments for v in e.course.videos]

    return jsonify([{
        'id': v.id,
        'course_id': v.course_id,
        'title': v.title,
        'description': v.description,
        'url': v.url,
        'upload_date': v.upload_date.isoformat()
    } for v in videos]), 200

@bp.route('/videos', methods=['POST'])
@login_required
def create_video():
    if current_user.user_type != 'Teacher':
        return jsonify({'message': 'Only teachers can upload videos'}), 403

    data = request.get_json()
    course = Course.query.get_or_404(data['course_id'])
    if course.teacher_id != current_user.id:
        return jsonify({'message': 'You can only upload videos to your own courses'}), 403

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
    return jsonify({
        'id': video.id,
        'course_id': video.course_id,
        'title': video.title,
        'description': video.description,
        'url': video.url,
        'upload_date': video.upload_date.isoformat()
    }), 200

@bp.route('/videos/<int:video_id>', methods=['PUT'])
@login_required
def update_video(video_id):
    if current_user.user_type != 'Teacher':
        return jsonify({'message': 'Only teachers can update videos'}), 403

    video = Video.query.get_or_404(video_id)
    if video.course.teacher_id != current_user.id:
        return jsonify({'message': 'You can only update your own videos'}), 403

    data = request.get_json()
    video.title = data.get('title', video.title)
    video.description = data.get('description', video.description)
    video.url = data.get('url', video.url)

    db.session.commit()
    return jsonify({'message': 'Video updated successfully'}), 200

@bp.route('/videos/<int:video_id>', methods=['DELETE'])
@login_required
def delete_video(video_id):
    if current_user.user_type != 'Teacher':
        return jsonify({'message': 'Only teachers can delete videos'}), 403

    video = Video.query.get_or_404(video_id)
    if video.course.teacher_id != current_user.id:
        return jsonify({'message': 'You can only delete your own videos'}), 403

    db.session.delete(video)
    db.session.commit()
    return jsonify({'message': 'Video deleted successfully'}), 200