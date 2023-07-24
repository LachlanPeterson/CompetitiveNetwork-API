from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import json

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

class Game(db.Model):
   __tablename__ = 'games'

   game_id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(50))
   description = db.Column(db.Text())
   genre = db.Column(db.String(50))
   rank_system = db.Column(db.Text())

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
   users = User(
      name = 'LachlanPeterson',
      email = 'LachlanPeterson@gmail.com',
      password = 'LPassword123',
      is_admin = True,
      date_created = date.today(),
   )
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
   db.session.add(users)
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
    return json.dumps(games)

# Testing SQL Queries - all fps games
@app.cli.command('fps_games')
def all_games():
# Showing all fps games in the competitive_network database
    stmt = db.select(Game).where(Game.genre == 'FPS - First Person Shooter').order_by(Game.title)
    games = db.session.scalars(stmt).all()
    for game in games:
        print(game.__dict__)


@app.route('/')
def index():
    return 'Competitive Rank Review Home'

if __name__ == '__main__':
    app.run(debug=True)