import os
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Exam, Question, Choice, StudentResponse, db
from datetime import datetime
import config
from werkzeug.utils import secure_filename

bp = Blueprint('exams', __name__)

UPLOAD_FOLDER = 'static/uploads/'  
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/exams')
@login_required
def exams_page():
    exams = Exam.query.filter_by(stage=current_user.stage).all()
    return render_template('External_pages/Exam.html', exams=exams)

@bp.route('/exams')
@login_required
def exam_detail(exam_id):
    exam = Exam.query.filter_by(exam_id)
    return render_template('External_pages/Exam_detail.html', exams=exam)

@bp.route('/submit_exam/<int:exam_id>', methods=['GET', 'POST'])
@login_required
def submit_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    
    # Check if the student has already started the exam
    student_response = StudentResponse.query.filter_by(student_id=current_user.id, exam_id=exam_id).first()
    
    if not student_response:
        # Create a new StudentResponse entry when the exam is first accessed
        student_response = StudentResponse(
            student_id=current_user.id,
            exam_id=exam_id,
            is_started=True,
            score=0,  # Set a default score here
            choices=''  # Initialize the choices as an empty string
        )
        db.session.add(student_response)
        db.session.commit()
    else:
        # Prevent access if the exam has already been submitted
        if student_response.score is not None:
            flash('You have already submitted this exam.', 'danger')
            return redirect(url_for('exams.exam_detail', exam_id=exam_id))

    if request.method == 'POST':
        score = 0
        choices = []

        # Parse the choices from the request
        data = request.get_json()
        for key, value in data.items():
            if key.startswith('question_'):
                question_id = key.split('_')[1]
                selected_choice = value
                choices.append(f'Q{question_id}:{selected_choice}')
                
                # Find the question and check if the selected choice is correct
                question = next((q for q in exam.questions if q.id == int(question_id)), None)
                if question and question.correct_answer == selected_choice:
                    score += 1

        # Convert choices list to a string and store it in the StudentResponse model
        choices_str = ','.join(choices)
        student_response.choices = choices_str

        # Calculate and store the score
        total_questions = len(exam.questions)
        result = (score / total_questions) * 100
        student_response.score = result

        db.session.commit()

        # Return JSON response
        return jsonify({'message': f'You scored {result:.2f}%' , 'redirect': url_for('exams.exam_detail', exam_id=exam_id)})

    # Render the exam page if GET request
    return render_template('External_pages/Exam_detail.html', exam=exam)


@bp.route('/add_exam', methods=['POST'])
@login_required
def add_exam():
    try:
        title = request.form.get('title')
        description = request.form.get('description')
        subject = request.form.get('subject')
        stage = request.form.get('stage')

        exam = Exam(
            title=title,
            description=description,
            subject=subject,
            stage=stage,
            user_id=current_user.id
        )
        db.session.add(exam)
        db.session.flush()  # Ensure the exam ID is available for questions

        # Process questions
        question_data = request.form.to_dict(flat=False)  # Use to_dict(flat=False) to get nested data
        
        print("Received question data:", question_data)  # Debugging line

        question_index = 0
        while f'questions[{question_index}][questionText]' in question_data:
            question_text = question_data.get(f'questions[{question_index}][questionText]', [None])[0]
            correct_answer = question_data.get(f'questions[{question_index}][correctAnswer]', [None])[0]
            
            question_image = request.files.get(f'questions[{question_index}][questionImage]')
            correct_answer_image = request.files.get(f'questions[{question_index}][correctAnswerImage]')

            if question_image and allowed_file(question_image.filename):
                filename = secure_filename(question_image.filename)
                question_image.save(os.path.join(config['UPLOAD_FOLDER'], filename))
                question_image_path = os.path.join(config['UPLOAD_FOLDER'], filename)
            else:
                question_image_path = None
            
            if correct_answer_image and allowed_file(correct_answer_image.filename):
                filename = secure_filename(correct_answer_image.filename)
                correct_answer_image.save(os.path.join(config['UPLOAD_FOLDER'], filename))
                correct_answer_image_path = os.path.join(config['UPLOAD_FOLDER'], filename)
            else:
                correct_answer_image_path = None

            question = Question(
                question_text=question_text,
                correct_answer=correct_answer,
                exam_id=exam.id,
                question_image=question_image_path,
                correct_answer_image=correct_answer_image_path
            )
            db.session.add(question)
            db.session.flush()  # Ensure the question ID is available for choices

            choice_index = 0
            while f'questions[{question_index}][choices][{choice_index}][text]' in question_data:
                choice_text = question_data.get(f'questions[{question_index}][choices][{choice_index}][text]', [None])[0]
                choice_image = request.files.get(f'questions[{question_index}][choices][{choice_index}][image]')

                if choice_image and allowed_file(choice_image.filename):
                    filename = secure_filename(choice_image.filename)
                    choice_image.save(os.path.join(config['UPLOAD_FOLDER'], filename))
                    choice_image_path = os.path.join(config['UPLOAD_FOLDER'], filename)
                else:
                    choice_image_path = None

                if choice_text:  # Ensure that choice text is present
                    choice = Choice(
                        choice_text=choice_text,
                        question_id=question.id,
                        choice_image=choice_image_path
                    )
                    db.session.add(choice)
                
                choice_index += 1

            question_index += 1

        db.session.commit()

        return jsonify({'success': True, 'message': 'Exam created successfully!'})
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while adding the exam. Please try again.', 'danger')
        print(str(e))  # Log the error for debugging
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
