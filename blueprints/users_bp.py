from flask import Blueprint, request
from models.user import User, UserSchema
from init import db
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required, admin_or_owner_required

users_bp = Blueprint('users', __name__, url_prefix='/users')

# Read all users
@users_bp.route('/', methods=['GET'])
@jwt_required()
def all_users():
    # Select * from users;
    stmt = db.select(User).order_by(User.user_id)
    users = db.session.scalars(stmt).all()
    return UserSchema(many=True, exclude=['password', 'games','date_created', 'ranks']).dump(users)

# Read one specific user and contains all Ranks & Games;
@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def one_user(user_id):
    stmt = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(stmt)
    if user:
        return UserSchema(exclude=['password', 'games','date_created']).dump(user)
    else:
        return {'error': 'User not found'}, 404
    
# Update a user
@users_bp.route('/<int:user_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(user_id):
    admin_required()
    stmt = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(stmt)
    user_info = UserSchema().load(request.json)
    if user:
        user.name = user_info.get('name', user.name)
        user.email = user_info.get('email', user.email)
        user.password = user_info.get('password', user.password)
        db.session.commit()
        return UserSchema(exclude=['password', 'date_created', 'games', 'ranks']).dump(user)
    else:
        return {'error': 'User not found'}, 404
    
# Delete a user
@users_bp.route('/<int:user_id>', methods=['DELETE'])
# Someone must be logged in
@jwt_required()
def delete_user(user_id):
    # Admin is required
    admin_required()
    stmt = db.select(User).filter_by(user_id=user_id)
    user = db.session.scalar(stmt)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'message': 'The User has been deleted'}, 200
    else:
        return {'error': 'User not found'}, 404
