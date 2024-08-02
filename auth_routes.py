from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flasgger import swag_from

from models import db, User, Role
from utils import send_reset_email,s

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'first_name': {'type': 'string'},
                    'last_name': {'type': 'string'},
                    'password': {'type': 'string'},
                    'email': {'type': 'string'}
                },
                'required': ['username', 'first_name', 'last_name', 'password', 'email']
            }
        }
    ],
    'responses': {
        201: {'description': 'User registered successfully'},
        400: {'description': 'Invalid input'}
    }
})
def register():
    data = request.json
    role_str = data.get('role', 'User').upper()
    if role_str not in Role.__members__:
        return jsonify({"message": "Invalid role"}), 400
    role = Role[role_str]
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        password=hashed_password,
        email=data['email'],
        role=role
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        200: {'description': 'Login successful'},
        401: {'description': 'Invalid credentials'}
    }
})
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route('/forgot-password', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'ForgotPassword',
                'required': ['email'],
                'properties': {
                    'email': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Password reset email sent'},
        400: {'description': 'Invalid email'}
    }
})
def forgot_password():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user:
        reset_url = send_reset_email(user)
    return jsonify({"message": "If the email is registered, a password reset link has been sent.","reset_url": reset_url}), 200

@auth_bp.route('/reset-password/<token>', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'parameters': [
        {
            'name': 'token',
            'in': 'path',
            'type': 'string',
            'required': True
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'ResetPassword',
                'required': ['password'],
                'properties': {
                    'password': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Password reset successful'},
        400: {'description': 'Invalid or expired token'}
    }
})
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        return jsonify({"message": "Invalid or expired token"}), 400

    data = request.json
    user = User.query.filter_by(email=email).first()
    if user:
        user.password = generate_password_hash(data['password'])
        db.session.commit()
        return jsonify({"message": "Password reset successful"}), 200
    return jsonify({"message": "User not found"}), 400