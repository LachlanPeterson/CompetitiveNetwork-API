from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)

# protocol + adapter + username and password @ the port
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://cn_dev:cndev123@localhost:5432/competitive_network'

# Open connection to database and intilized alchemy
db = SQLAlchemy(app)

# User Entity model for Users
class User(db.Model):
  __tablename__ = 'users'
  
  user_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(16)) # name 16 characters max
  email = db.Column(db.String(50))
  password = db.Column(db.String(50))
  is_admin = db.Column(db.Boolean(True))
  date_created = db.Column(db.Date())

# Cli command to create tables
@app.cli.command('create')
def create_db():
   db.drop_all()
   db.create_all()
   print('Testing table creation')

# Cli command to seed tables
@app.cli.command('seed')
def seed_db():
   users = User(
      name = 'LachlanPeterson',
      email = 'LachlanPeterson@gmail.com',
      password = 'LPassword123',
      is_admin = True,
      date_created = date.today(),
   )

#    Truncate the User table
   db.session.query(User).delete()

#    Add the user to the session (transaction)
   db.session.add(users)

#    Commit the transaction to the database
   db.session.commit()
   print('Models seeded')


@app.route('/')
def index():
    return 'Competitive Rank Review Home'

if __name__ == '__main__':
    app.run(debug=True)