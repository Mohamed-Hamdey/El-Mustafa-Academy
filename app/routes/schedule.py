from flask import Blueprint, render_template, request, redirect, url_for
from app.models import db, Schedule

bp = Blueprint('schedule', __name__, url_prefix='/schedule')

@bp.route('/')
def index():
    schedules = Schedule.query.all()
    return render_template('External_pages/schedule.html', schedules=schedules)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Handle form submission
        new_schedule = Schedule(
            title=request.form['title'],
            description=request.form['description'],
            date=request.form['date']
        )
        db.session.add(new_schedule)
        db.session.commit()
        return redirect(url_for('schedule.index'))
    return render_template('schedule/add.html')

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    schedule = Schedule.query.get_or_404(id)
    db.session.delete(schedule)
    db.session.commit()
    return redirect(url_for('schedule.index'))