from flask import Blueprint
from datetime import date
from models.user import User
from models.game import Game
from init import db, bcrypt

cli_bp = Blueprint('db', __name__)

# Create Tables
@cli_bp.cli.command('create')
def create_db():
   db.drop_all()
   db.create_all()
   print('Tables created successfully')

# Seed Tables
@cli_bp.cli.command('seed')
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
   #    Create instance of the Game model in memory
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


# Testing SQL Queries - all fps games
@cli_bp.cli.command('fps_games')
def all_games():
# Showing all fps games in the competitive_network database
    stmt = db.select(Game).where(Game.genre == 'FPS - First Person Shooter').order_by(Game.title)
    games = db.session.scalars(stmt).all()
    for game in games:
        print(game.__dict__)