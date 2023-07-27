from flask import Blueprint, request, abort
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity
from models.user import User, UserSchema
from init import db, bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Admin required function
def admin_required():
   # Using jwt auth to validate admin user by retrieving JSON webtoken and comparing it against user_id
   user_id = get_jwt_identity()
   stmt = db.select(User).filter_by(user_id=user_id) # Build query
   user = db.session.scalar(stmt) # Execute query
   # Check if the user and admin exist and are true, otherwise abort and send error
   if not (user and user.is_admin):
      abort(401, description='You must be an admin')

# Register/create a new user
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
      return UserSchema(exclude=['password', 'date_created']).dump(user), 201
   except IntegrityError:
      return {'error': 'Email address is already registered'}, 409
   except KeyError:
      return {'error': 'Name, Email and Password are required'}, 400


# Login as a user
@auth_bp.route('/login', methods=['POST'])
def login():
   try:
      # Select a valid user from the db by matching an email address
      stmt = db.select(User).filter_by(email=request.json['email']) #Build Query
      user = db.session.scalar(stmt) #Execute Query
      # Check if the user exists and the password given by the user corresponds to the database (matches)
      # If it matches create an acess token.
      if user and bcrypt.check_password_hash(user.password, request.json['password']):
         token = create_access_token(identity=user.user_id, expires_delta=timedelta(days=1))
         return {'token': token, 'user': UserSchema(exclude=['password', 'games', 'ranks', 'date_created']).dump(user)}
      else:
         return {'error': 'Invalid email address or password'}, 401 #If the email or password provided dont match the db, return an error.
   except KeyError:
      return {'error': 'Email and password are required'}, 400 # If the required fields are missing, return an error