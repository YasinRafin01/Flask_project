from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from models import db, User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/user', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['User'],
    'security': [{'JWT': []}],
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'JWT token in the format: Bearer <token>'
        }
    ],
    'responses': {
        200: {
            'description': 'User profile retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'first_name': {'type': 'string'},
                    'last_name': {'type': 'string'},
                    'email': {'type': 'string'},
                    'role': {'type': 'string'},
                    'active': {'type': 'boolean'}
                }
            }
        },
        401: {'description': 'Unauthorized'}
    }
})
def get_user_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role.value,
        "active": user.active
    }), 200

@user_bp.route('/user', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['User'],
    'security': [{'JWT': []}],
    'parameters': [
        {
            'name': 'Authorization',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'JWT token in the format: Bearer <token>'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'first_name': {'type': 'string'},
                    'last_name': {'type': 'string'},
                    'email': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'User profile updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        401: {'description': 'Unauthorized'},
        405: {'description': 'User not allowed to change role'}
    }
})
def update_user_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    data = request.json
    if 'role' in data:
        return jsonify({"message": "User not allowed to change role"}), 405
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200