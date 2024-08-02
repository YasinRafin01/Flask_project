from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from models import db, User, Role

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/admin/users', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Admin'],
    'security': [{'JWT': []}],
    'responses': {
        200: {'description': 'List of all users'}
    }
})
def admin_get_users():
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != Role.ADMIN:
        return jsonify({"message": "Unauthorized"}), 403
    
    users = User.query.all()
    return jsonify([{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role.value,
        "active": user.active
    } for user in users]), 200

@admin_bp.route('/admin/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Admin'],
    'security': [{'JWT': []}],
    'parameters': [
        {'name': 'user_id', 'in': 'path', 'type': 'integer', 'required': True},
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
                    'email': {'type': 'string'},
                    'role': {'type': 'string'},
                    'active': {'type': 'boolean'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'User updated successfully'},
        404: {'description': 'User not found'},
        403: {'description': 'Unauthorized'},
        400: {'description': 'Email already in use'}
    }
})
def admin_update_user(user_id):
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != Role.ADMIN:
        return jsonify({"message": "Unauthorized"}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    # Ensure an admin cannot update or delete another admin
    if user.role == Role.ADMIN and current_user.id != user.id:
        return jsonify({"message": "Unauthorized to manage another admin"}), 403
    
    data = request.json
    new_email = data.get('email', user.email)
    
    # Check for unique email
    if User.query.filter_by(email=new_email).filter(User.id != user_id).first():
        return jsonify({"message": "Email already in use"}), 400
    
    user.username = data.get('username', user.username)
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = new_email
    user.role = Role(data.get('role', user.role.value))
    user.active = data.get('active', user.active)
    db.session.commit()
    return jsonify({"message": "Updated successfully"}), 200

@admin_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'tags': ['Admin'],
    'security': [{'JWT': []}],
    'parameters': [
        {'name': 'user_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'User deleted successfully'},
        404: {'description': 'User not found'},
        403: {'description': 'Unauthorized'}
    }
})
def admin_delete_user(user_id):
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != Role.ADMIN:
        return jsonify({"message": "Unauthorized"}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    # Ensure an admin cannot update or delete another admin
    if user.role == Role.ADMIN and current_user.id != user.id:
        return jsonify({"message": "Unauthorized to manage another admin"}), 403
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"}), 200

@admin_bp.route('/admin/users/<int:user_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Admin'],
    'security': [{'JWT': []}],
    'parameters': [
        {'name': 'user_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {
            'description': 'User details retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'username': {'type': 'string'},
                    'first_name': {'type': 'string'},
                    'last_name': {'type': 'string'},
                    'email': {'type': 'string'},
                    'role': {'type': 'string'},
                    'active': {'type': 'boolean'}
                }
            }
        },
        403: {'description': 'Unauthorized'},
        404: {'description': 'User not found'}
    }
})
def admin_get_unique_user(user_id):
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != Role.ADMIN:
        return jsonify({"message": "Unauthorized"}), 403


    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    if user.role == Role.ADMIN and current_user.id != user.id:
        return jsonify({"message": "Unauthorized to manage another admin"}), 403

    return jsonify({
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role.value,
        "active": user.active
    }), 200