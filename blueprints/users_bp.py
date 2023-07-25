from flask import Blueprint
from models.user import User, UserSchema
from init import db
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required

users_bp = Blueprint('users', __name__)

@users_bp.route('/users')
@jwt_required()
def all_users():
    admin_required()

    # Select * from users;
    stmt = db.select(User).order_by(User.name)
    users = db.session.scalars(stmt).all()
    return UserSchema(many=True, exclude=['password']).dump(users)