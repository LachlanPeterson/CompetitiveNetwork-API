from flask import Blueprint, request
from models.user import User, UserSchema
from init import db
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required, admin_or_owner_required

users_bp = Blueprint('users', __name__, url_prefix='/users')

# Get/Read all users;
@users_bp.route('/', methods=['GET'])
@jwt_required()
def all_users():
    stmt = db.select(User).order_by(User.user_id) # Preps query to retrieve all useres ordered by user_id
    users = db.session.scalars(stmt).all() # Executes query
    return UserSchema(many=True, exclude=['password', 'games','date_created', 'ranks']).dump(users) # Dumps all users, with chosen fields excluded

# Get/Read a specific user;
@users_bp.route('/<int:user_id>', methods=['GET']) 
@jwt_required()
def one_user(user_id):
    stmt = db.select(User).filter_by(user_id=user_id) # Preps query to get a user with the matching user_id passed into the route
    user = db.session.scalar(stmt) # Executes the query
    if user: # If the user exists, the return the user schema excluding hte fields mentioned
        return UserSchema(exclude=['password', 'games','date_created']).dump(user)
    else:
        return {'error': 'User not found'}, 404 # If no user exists, return an error
    
# Update (PUT/PATCH) a specific user;
@users_bp.route('/<int:user_id>', methods=['PUT', 'PATCH'])
@jwt_required() # Get the JWT Token from the request to validate a user is logged in
def update_user(user_id):
    admin_required() #Validate token against user to see whether they are admin
    stmt = db.select(User).filter_by(user_id=user_id) # Prep query to find user with a matching user_id to the passed in value
    user = db.session.scalar(stmt) # Executes query
    user_info = UserSchema().load(request.json) # Deserialises JSON data in request to convert into python object
    if user:
        user.name = user_info.get('name', user.name) # Update name if changed
        user.email = user_info.get('email', user.email) # Update email if changed
        user.password = user_info.get('password', user.password) # Update password if changed
        db.session.commit() # Commit the changes to the database
        return UserSchema(exclude=['password', 'date_created', 'games', 'ranks']).dump(user) # Return updated user schema excluding specific fields
    else:
        return {'error': 'User not found'}, 404 # If user is not in the database, return an error message 
    
# Delete a specific user;
@users_bp.route('/<int:user_id>', methods=['DELETE'])
# Someone must be logged in
@jwt_required() # Get the JWT Token from the request
def delete_user(user_id):
    # Admin is required
    admin_required()
    stmt = db.select(User).filter_by(user_id=user_id) # Prep query to find matching user from database with the same user_id passed in
    user = db.session.scalar(stmt) # Execute query
    if user: # If the user exists continue the request
        db.session.delete(user) # Delete the user from the database
        db.session.commit() # Commit the changes to the database
        return {'message': 'The User has been deleted'}, 200 # Return confirmation message
    else:
        return {'error': 'User not found'}, 404 # If the user is not found, return error message
