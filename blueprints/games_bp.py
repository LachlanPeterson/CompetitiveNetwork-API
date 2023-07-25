from flask import Blueprint
from models.game import Game, GameSchema
from init import db

games_bp = Blueprint('games', __name__)

# Turning all games query into a Route
@games_bp.route('/games')
def all_games():
# Select * from games; 
# Showing all games in the competitive_network database
    stmt = db.select(Game).order_by(Game.title)
    games = db.session.scalars(stmt).all()
    return GameSchema(many=True).dump(games)