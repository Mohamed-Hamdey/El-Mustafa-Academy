from flask import Blueprint, render_template, request, jsonify, url_for, redirect
from flask_login import login_user, current_user, login_required
from app.models import User, db

bp = Blueprint('auth', __name__)

@bp.route('/', methods=['POST'])
def handle_auth():
    data = request.get_json()
    
    if 'email' in data:  # Registration
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists'}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400

        user = User(
            username=data['username'],
            email=data['email'],
            stage=data.get('stage'),
            phone_number=data.get('phone_number'),
            status='pending'  # Mark as pending
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully, pending approval'}), 201

    else:  # Login
        if 'username' not in data or 'password' not in data:
            return jsonify({'message': 'Username and password are required'}), 400

        user = User.query.filter_by(username=data['username']).first()

        if user and user.check_password(data['password']):
            print("User status before approval:", user.status)

            # Directly log in 'mohamed_mostafa_' and redirect to the dashboard
            if user.username == 'mohamed_mostafa_':
                login_user(user)
                return jsonify({'redirect': url_for('auth.dashboard')}), 200

            # Automatically approve the user if their status is pending
            if user.status == 'pending':
                user.status = 'approved'
                db.session.commit()
                # Reload the user object from the database to ensure status is updated
                user = User.query.filter_by(username=data['username']).first()
                print("User status after approval:", user.status)

            # Check the updated status for other users
            if user.status == 'approved':
                login_user(user)
                return jsonify({'redirect': url_for('auth.home')}), 200
            else:
                print("Account not approved yet")
                return jsonify({'message': 'Your account is not approved yet'}), 403
        else:
            print("Invalid username or password")
            return jsonify({'message': 'Invalid username or password'}), 401

@bp.route('/home/')
@login_required
def home():
    return render_template('Home.html')

@bp.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@bp.route('/pending_requests/')
@login_required
def pending_requests():
    if current_user.username == 'mohamed_mostafa_':
        # Automatically approve the teacher's own status
        if current_user.status == 'pending':
            current_user.status = 'approved'
            db.session.commit()  # Only allow the teacher to view pending requests
        pending_users = User.query.filter_by(status='pending').all()
        return render_template('pending_requests.html', pending_users=pending_users)
    else:
        return redirect(url_for('auth.home'))

@bp.route('/handle_request/', methods=['POST'])
@login_required
def handle_request():
    if current_user.username == 'mohamed_mostafa_':
        data = request.get_json()
        user = User.query.get(data['user_id'])

        if data['action'] == 'accept':
            user.status = 'approved'
            db.session.commit()
            return jsonify({'message': 'User approved successfully'})
        elif data['action'] == 'reject':
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User rejected and deleted successfully'})
        else:
            return jsonify({'message': 'Invalid action'}), 400
    else:
        return jsonify({'message': 'Unauthorized'}), 403
