from flask import Blueprint, render_template, request, redirect, url_for
from app.models import db, Notification

bp = Blueprint('notifications', __name__, url_prefix='/notifications')

@bp.route('/')
def index():
    notifications = Notification.query.all()
    return render_template('notifications/index.html', notifications=notifications)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Handle form submission
        new_notification = Notification(
            message=request.form['message'],
            date=request.form['date']
        )
        db.session.add(new_notification)
        db.session.commit()
        return redirect(url_for('notifications.index'))
    return render_template('notifications/add.html')

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    notification = Notification.query.get_or_404(id)
    db.session.delete(notification)
    db.session.commit()
    return redirect(url_for('notifications.index'))