from flask import Blueprint, request, abort
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity
from models.user import User, UserSchema
from init import db, bcrypt

auth_bp = Blueprint('auth', __name__)

# Admin required function
def admin_required():
   # Using jwt auth to validate admin user
   user_id = get_jwt_identity()
   stmt = db.select(User).filter_by(user_id=user_id)
   user = db.session.scalar(stmt)
   if not (user and user.is_admin):
      abort(401)

def admin_or_owner_required(owner_id):
   # Using jwt auth to validate admin user
   user_id = get_jwt_identity()
   stmt = db.select(User).filter_by(user_id=user_id)
   user = db.session.scalar(stmt)
   if not (user and (user.is_admin or user_id == owner_id)):
      abort(401)


# Register Endpoint
@auth_bp.route('/register', methods=['POST'])
def register():
   try:
      # Parse, sanitize and validate the incoming JSON data
      # via the schema
      user_info = UserSchema().load(request.json)
      # Create a new User model instance with the schema data
      user = User(
         name = user_info['name'],
         email = user_info['email'],
         password = bcrypt.generate_password_hash(user_info['password']).decode('utf-8')
      )
      
      # Add and commit the new user to the database
      db.session.add(user)
      db.session.commit()

      # Return the new user, excluding the password
      return UserSchema(exclude=['password']).dump(user), 201
   except IntegrityError:
      return {'error': 'Email address is already registered'}, 409


# Login Endpoint
@auth_bp.route('/login', methods=['POST'])
def login():
   try:
      stmt = db.select(User).filter_by(email=request.json['email'])
      user = db.session.scalar(stmt)
      if user and bcrypt.check_password_hash(user.password, request.json['password']):
         token = create_access_token(identity=user.user_id, expires_delta=timedelta(days=7))
         return {'token': token, 'user': UserSchema(exclude=['password', 'games', 'ranks', 'date_created']).dump(user)}
      else:
         return {'error': 'Invalid email address or password'}, 401
   except KeyError:
      return {'error': 'Email and password are required'}, 400