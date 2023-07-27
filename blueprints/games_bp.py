from flask import Blueprint, request
from models.game import Game, GameSchema
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required
from datetime import date

games_bp = Blueprint('games', __name__, url_prefix='/games')


# POST/Create a games;
@games_bp.route('/', methods=['POST'])
@jwt_required() # Get the JWT Token from the request to validate a user is logged in
def create_game():
    admin_required() #Validate token against user to see whether they are admin
    game_info = GameSchema().load(request.json) # Load the incoming POST data via the schema
    # Created a new Game instance from the game_info
    game = Game(
        title = game_info['title'],
        description = game_info['description'],
        genre = game_info['genre'],
        date_created = date.today(),
        user_id = get_jwt_identity()
    )
    
    db.session.add(game) # Add and commit the new game to the session
    db.session.commit()
    return GameSchema().dump(game), 201 # Return updated GameSchema 


# Get/Read all games;
@games_bp.route('/', methods=['GET'])
def all_games(): 
    stmt = db.select(Game).order_by(Game.game_id) # Prep query to get all games, ordering it by game_id
    games = db.session.scalars(stmt).all() # Executes the query
    return GameSchema(many=True, exclude=['ranks', 'user']).dump(games) # Return updated GameSchema excluding specific fields


# Get/Read one specific game;
@games_bp.route('/<int:game_id>', methods=['GET'])
@jwt_required() # Get the JWT Token from the request
def one_game(game_id):
    stmt = db.select(Game).filter_by(game_id=game_id) # Preps query to get a game with the matching game_id passed into the route
    game = db.session.scalar(stmt) # Executes the query
    if game: # If the game exists, return the Game schema
        return GameSchema().dump(game)
    else:
        return {'error': 'Game not found'}, 404 #If no game exists, return an error


# Update (PUT/PATCH) a specific game;
@games_bp.route('/<int:game_id>', methods=['PUT', 'PATCH'])
@jwt_required() # Get the JWT Token from the request
def update_game(game_id):
    admin_required() #Validate token against user to see whether they are admin
    stmt = db.select(Game).filter_by(game_id=game_id) # Prep query to find a game with a matching game_id to the passed in value
    game = db.session.scalar(stmt) # Executes query
    game_info = GameSchema().load(request.json) # Deserialises JSON data in request to convert into python object
    if game:
        game.title = game_info.get('title', game.title) # Update title if changed
        game.description = game_info.get('description', game.description) # Update description if changed
        game.genre = game_info.get('genre', game.genre) # Update genre if changed
        db.session.commit() # Commit model changes to database
        return GameSchema().dump(game) # Return updated GameSchema 
    else:
        return {'error': 'Game not found'}, 404 # If no game is found, return error

# Delete a specific game;
@games_bp.route('/<int:game_id>', methods=['DELETE'])
# Someone must be logged in
@jwt_required() # Get the JWT Token from the request
def delete_game(game_id):
    # Admin is required
    admin_required() #Validate token against user to see whether they are admin
    stmt = db.select(Game).filter_by(game_id=game_id) # Prep query to find a game with a matching game_id to the passed in value
    game = db.session.scalar(stmt) # Execute query
    if game: # If the game exists continue the request
        db.session.delete(game) # Delete the game from the database
        db.session.commit() # Commit the changes to the database
        return {'message': 'The Game has been deleted'}, 200 # Return confirmation message
    else:
        return {'error': 'Game not found'}, 404 # If the game is not found, return error message