from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from os import environ
from dotenv import load_dotenv
from models.user import User, UserSchema
from models.game import Game, GameSchema
from init import db, ma, bcrypt, jwt

load_dotenv()

app = Flask(__name__)

# protocol + adapter + username and password @ the port
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')

# Giving app.py the instance of app from init
db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

def admin_required():
   # Using jwt auth to validate admin user
   user_email = get_jwt_identity()
   stmt = db.select(User).filter_by(email=user_email)
   user = db.session.scalar(stmt)
   if not (user and user.is_admin):
      abort(401)

@app.errorhandler(401)
def unauthorized(err):
   return {'error': 'You must be an admin'}, 401

# Cli command to create tables
@app.cli.command('create')
def create_db():
   db.drop_all()
   db.create_all()
   print('Tables created successfully')

# Cli command to seed tables
@app.cli.command('seed')
def seed_db():
#    Create instance of the User model in memory
   users = [
      User(
            name = 'Lachlan Peterson',
            email = 'LachlanPeterson@gmail.com',
            password = bcrypt.generate_password_hash('LPassword123').decode('utf-8'),
            date_created = date.today(),
            is_admin = True,
         ),
         User(
            name = 'Regular User',
            email = 'regular_user@gmail.com',
            password = bcrypt.generate_password_hash('RUser123').decode('utf-8'),
            date_created = date.today(),
         ),
   ]
   
   games = [
      Game(
            title = 'League of Legends',
            description = 'LoL Description',
            genre = 'MOBA - Multiplayer Online Battle Arena',
            rank_system = "Rank system filler"
        ),
        Game(
            title = 'Valorant',
            description = 'Valorant Description',
            genre = 'FPS - First Person Shooter',
            rank_system = "Rank system filler"
        ),
        Game(
            title = 'CS:GO - Counter Strike Global Offensive',
            description = 'CS:GO Description',
            genre = 'FPS - First Person Shooter',
            rank_system = "Rank system filler"
        ),
   ]
    
        
#    Truncate the User table
   db.session.query(User).delete()
   db.session.query(Game).delete()

#    Add the user or new card to the session (transaction)
   db.session.add_all(users)
   db.session.add_all(games)

#    Commit the transaction to the database
   db.session.commit()
   print('Models seeded')


# Turning all games query into a Route
@app.route('/games')
def all_games():
# Select * from games; 
# Showing all games in the competitive_network database
    stmt = db.select(Game).order_by(Game.title)
    games = db.session.scalars(stmt).all()
    return GameSchema(many=True).dump(games)

# Testing SQL Queries - all fps games
@app.cli.command('fps_games')
def all_games():
# Showing all fps games in the competitive_network database
    stmt = db.select(Game).where(Game.genre == 'FPS - First Person Shooter').order_by(Game.title)
    games = db.session.scalars(stmt).all()
    for game in games:
        print(game.__dict__)

# Register Endpoint, only want to accept post requests
@app.route('/register', methods=['POST'])
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

@app.route('/login', methods=['POST'])
def login():
   try:
      stmt = db.select(User).filter_by(email=request.json['email'])
      user = db.session.scalar(stmt)
      if user and bcrypt.check_password_hash(user.password, request.json['password']):
         token = create_access_token(identity=user.email, expires_delta=timedelta(days=7))
         return {'token': token, 'user': UserSchema(exclude=['password']).dump(user)}
      else:
         return {'error': 'Invalid email address or password'}, 401
   except KeyError:
      return {'error': 'Email and password are required'}, 400
   
@app.route('/users')
@jwt_required()
def all_users():
    admin_required()

    # Select * from users;
    stmt = db.select(User).order_by(User.name)
    users = db.session.scalars(stmt).all()
    return UserSchema(many=True, exclude=['password']).dump(users)

@app.route('/')
def index():
    return 'Competitive Rank Review Home'

if __name__ == '__main__':
    app.run(debug=True)