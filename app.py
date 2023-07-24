from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# protocol + adapter + username and password @ the port
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://cn_dev:cndev123@localhost:5432/competitive_network'

# Open connection to database
db = SQLAlchemy(app)

# User Entity
class User(db.Model):
  user_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(16)) # name 16 characters max
  email = db.Column(db.String(50))
  password = db.Column(db.String(50))
  is_admin = db.Column(db.Boolean(True))
  date_created = db.Column(db.Date())

# Cli command to create tables
@app.cli.command('create')
def create_db():
   db.create_all()
   print('Testing table creation')

@app.route('/')
def index():
    return 'Competitive Rank Review Home'

if __name__ == '__main__':
    app.run(debug=True)