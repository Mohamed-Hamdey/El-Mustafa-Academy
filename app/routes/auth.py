from flask import Blueprint, render_template, request, jsonify, url_for
from flask_login import login_user
from app.models import User, db

bp = Blueprint('auth', __name__)

@bp.route('/', methods=['POST'])
def handle_auth():
    data = request.get_json()

    # Check if it's a registration or login attempt
    if 'user_type' in data:  # Registration
        # Check for existing username
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists'}), 400

        # Check for existing email
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400

        # Create a new user
        user = User(
            username=data['username'],
            email=data['email'],
            user_type=data['user_type'],
            stage=data.get('stage'),
            phone_number=data.get('phone_number')
        )
        user.set_password(data['password'])

        # Save the user to the database
        db.session.add(user)
        db.session.commit()

        # Log the user in
        login_user(user)

        return jsonify({'message': 'User registered successfully', 'redirect': url_for('auth.home')}), 201

    else:  # Login
        user = User.query.filter_by(username=data['username'], user_type=data['user_type']).first()

        if user and user.check_password(data['password']):
            login_user(user)
            return jsonify({'message': 'Login successful', 'redirect': url_for('auth.home')}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401


@bp.route('/home/')
def home():
    return render_template('Home.html')  # Update with your actual home template path
