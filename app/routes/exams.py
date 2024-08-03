import os
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Exam, Question, Choice, StudentResponse, db
from datetime import datetime

bp = Blueprint('exams', __name__)

@bp.route('/exams')
@login_required
def exams_page():
    exams = Exam.query.filter_by(stage=current_user.stage).all()
    return render_template('External_pages/Exam.html', exams=exams)

@bp.route('/submit_exam/<int:exam_id>', methods=['POST'])
@login_required
def submit_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    if exam.stage != current_user.stage:
        return jsonify({'message': 'Unauthorized access'}), 403

    score = 0
    for question in exam.questions:
        selected_choice = request.form.get(f'question_{question.id}')
        if selected_choice and question.correct_answer == selected_choice:
            score += 1

    total_questions = len(exam.questions)
    result = (score / total_questions) * 100

    student_response = StudentResponse(
        student_id=current_user.id,
        exam_id=exam_id,
        score=result
    )
    db.session.add(student_response)
    db.session.commit()

    flash(f'You scored {result:.2f}%', 'success')
    return redirect(url_for('exams.exams_page'))

@bp.route('/add_exam', methods=['POST'])
@login_required
def add_exam():
    if not current_user.is_teacher:
        return jsonify({'message': 'Unauthorized access'}), 403

    title = request.form['title']
    description = request.form['description']
    subject = request.form['subject']
    stage = request.form['stage']

    exam = Exam(
        title=title,
        description=description,
        subject=subject,
        stage=stage,
        user_id=current_user.id
    )
    db.session.add(exam)
    db.session.commit()

    flash('Exam created successfully!', 'success')
    return redirect(url_for('exams.exams_page'))

@bp.route('/add_question/<int:exam_id>', methods=['POST'])
@login_required
def add_question(exam_id):
    if not current_user.is_teacher:
        return jsonify({'message': 'Unauthorized access'}), 403

    exam = Exam.query.get_or_404(exam_id)

    question_text = request.form['question_text']
    correct_answer = request.form['correct_answer']
    choices = request.form.getlist('choices')

    question = Question(
        question_text=question_text,
        correct_answer=correct_answer,
        exam_id=exam.id
    )
    db.session.add(question)
    db.session.flush()  # Get the question ID before adding choices

    for choice_text in choices:
        choice = Choice(
            choice_text=choice_text,
            question_id=question.id
        )
        db.session.add(choice)

    db.session.commit()

    flash('Question and choices added successfully!', 'success')
    return redirect(url_for('exams.exams_page', exam_id=exam_id))

# Error handlers
@bp.errorhandler(404)
def not_found_error(error):
    return render_template('error/404.html'), 404

@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error/500.html'), 500
