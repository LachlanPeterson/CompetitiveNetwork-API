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
from blueprints.cli_bp import cli_bp
from blueprints.auth_bp import auth_bp

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

app.register_blueprint(cli_bp)
app.register_blueprint(auth_bp)


# Turning all games query into a Route
@app.route('/games')
def all_games():
# Select * from games; 
# Showing all games in the competitive_network database
    stmt = db.select(Game).order_by(Game.title)
    games = db.session.scalars(stmt).all()
    return GameSchema(many=True).dump(games)




   
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