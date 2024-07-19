from flask import Blueprint, request, jsonify, render_template, url_for
from flask_login import login_required, current_user
from app.models import Video, db

bp = Blueprint('videos', __name__)

@bp.route('/videos/page', methods=['GET'])
@login_required
def video_page():
    return student_video_page()

@bp.route('/videos', methods=['GET'])
@login_required
def get_videos():
    videos = Video.query.filter_by(stage=current_user.stage).all()  # Filter by user's stage
    return jsonify([{
        'id': v.id,
        'title': v.title,
        'description': v.description,
        'upload_date': v.upload_date.isoformat(),
        'subject': v.subject,
        'file_path': v.file_path,
        'video_page': url_for('videos.get_video', video_id=v.id)
    } for v in videos]), 200

@bp.route('/videos/create', methods=['POST'])
@login_required
def create_video():
    data = request.get_json()
    video = Video(
        title=data['title'],
        description=data['description'],
        subject=data['subject'],
        stage=data['stage'],  # Added stage field
        file_path=data['file_path'],
        user_id=current_user.id
    )
    db.session.add(video)
    db.session.commit()
    return jsonify({'message': 'Video uploaded successfully', 'id': video.id}), 201

@bp.route('/videos/<int:video_id>', methods=['GET'])
@login_required
def get_video(video_id):
    video = Video.query.get_or_404(video_id)
    if video.stage != current_user.stage:
        return render_template('error/403.html')  # User should not access videos not in their stage

    if video.views >= video.max_views:
        return render_template('error/403.html')

    video.views += 1
    db.session.commit()

    return jsonify({
        'id': video.id,
        'title': video.title,
        'description': video.description,
        'upload_date': video.upload_date.isoformat(),
        'subject': video.subject,
        'file_path': video.file_path
    }), 200

@bp.route('/videos/<int:video_id>/update', methods=['PUT'])
@login_required
def update_video(video_id):
    video = Video.query.get_or_404(video_id)

    data = request.get_json()
    video.title = data.get('title', video.title)
    video.description = data.get('description', video.description)
    video.file_path = data.get('file_path', video.file_path)
    video.stage = data.get('stage', video.stage)  # Added stage field

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
    return render_template('dashboard.html')

@bp.route('/student/videos', methods=['GET'])
@login_required
def student_video_page():
    videos = Video.query.filter_by(stage=current_user.stage).all()  # Filter by user's stage
    return render_template('External_pages/video.html', videos=videos)
