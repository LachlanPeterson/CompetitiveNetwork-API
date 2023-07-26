from flask import Blueprint, request
from models.game import Game, GameSchema
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required
from datetime import date

games_bp = Blueprint('games', __name__, url_prefix='/games')

# C in CRUD
# Create a new game - same route as get all(but post method)
@games_bp.route('/', methods=['POST'])
# Someone must be logged in
@jwt_required()
def create_game():
    admin_required()
    # Load the incoming POST data via the schema
    game_info = GameSchema().load(request.json)
    # Created a new Game instance from the game_info
    game = Game(
        title = game_info['title'],
        description = game_info['description'],
        genre = game_info['genre'],
        date_created = date.today(),
        user_id = get_jwt_identity()
    )
    # Add and commit the new game to the session
    db.session.add(game)
    db.session.commit()
    # Send the new game back to the client
    return GameSchema().dump(game), 201

# R in CRUD - Two routes (All and One)
# Read/Get all games
@games_bp.route('/', methods=['GET'])
def all_games():
# Select * from games; 
# Showing all games in the competitive_network database
    stmt = db.select(Game).order_by(Game.game_id)
    games = db.session.scalars(stmt).all()
    return GameSchema(many=True, exclude=['ranks', 'user']).dump(games)


# Read/Get one specific game;
@games_bp.route('/<int:game_id>', methods=['GET'])
@jwt_required()
def one_game(game_id):
    # Selecting the Game, where the incoming game_id equals the id from the Model
    stmt = db.select(Game).filter_by(game_id=game_id)
    game = db.session.scalar(stmt)
    if game:
        return GameSchema().dump(game)
    else:
        return {'error': 'Game not found'}, 404

# U in CRUD
# Update a game
@games_bp.route('/<int:game_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_game(game_id):
    admin_required()
    stmt = db.select(Game).filter_by(game_id=game_id)
    game = db.session.scalar(stmt)
    game_info = GameSchema().load(request.json)
    if game:
        game.title = game_info.get('title', game.title)
        game.description = game_info.get('description', game.description)
        game.genre = game_info.get('genre', game.genre)
        # Commit model changes to database
        db.session.commit()
        return GameSchema().dump(game)
    else:
        return {'error': 'Game not found'}, 404
    
# D in CRUD
# Delete a game
@games_bp.route('/<int:game_id>', methods=['DELETE'])
# Someone must be logged in
@jwt_required()
def delete_game(game_id):
    # Admin is required
    admin_required()
    stmt = db.select(Game).filter_by(game_id=game_id)
    game = db.session.scalar(stmt)
    if game:
        db.session.delete(game)
        db.session.commit()
        return {'message': 'The Game has been deleted'}, 200
    else:
        return {'error': 'Game not found'}, 404