from flask import Blueprint, render_template, request, jsonify, url_for
from flask_login import login_user, current_user, login_required
from app.models import User, db

bp = Blueprint('auth', __name__)

@bp.route('/', methods=['POST'])
def handle_auth():
    data = request.get_json()

    # Check if the request data includes an email field to determine if it's a registration attempt
    if 'email' in data:  # Registration
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
        # Ensure that both username and password are provided
        if 'username' not in data or 'password' not in data:
            return jsonify({'message': 'Username and password are required'}), 400

        user = User.query.filter_by(username=data['username']).first()

        if user and user.check_password(data['password']):
            login_user(user)

            # Redirect logic based on username
            if user.username == 'mohamed_mostafa_':
                return jsonify({'message': 'Login successful', 'redirect': url_for('auth.dashboard')}), 200
            else:
                return jsonify({'message': 'Login successful', 'redirect': url_for('auth.home')}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401


@bp.route('/home/')
@login_required
def home():
    return render_template('Home.html')


@bp.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')
