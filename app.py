from flask import Flask
from os import environ
from dotenv import load_dotenv
from init import db, ma, bcrypt, jwt
from blueprints.cli_bp import cli_bp
from blueprints.auth_bp import auth_bp
from blueprints.users_bp import users_bp
from blueprints.games_bp import games_bp

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

@app.errorhandler(401)
def unauthorized(err):
   return {'error': 'You must be an admin'}, 401

app.register_blueprint(cli_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(games_bp)

# Wouldn't have a home route in API unless theres a few general routes
# @app.route('/')
# def index():
#     return 'Competitive Rank Review Home'

if __name__ == '__main__':
    app.run(debug=True)