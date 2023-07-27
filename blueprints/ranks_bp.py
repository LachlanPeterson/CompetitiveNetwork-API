from flask import Blueprint, request
from models.rank import Rank, RankSchema
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.auth_bp import admin_required
from datetime import date

ranks_bp = Blueprint('ranks', __name__, url_prefix='/ranks')

# Create new rank
@ranks_bp.route('/', methods=['POST'])
@jwt_required()
def create_rank():
    admin_required()
    rank_info = RankSchema().load(request.json)
    rank = Rank(
        rank_info['rank'],
        date_created = date.today(),
        user_id = get_jwt_identity(),
        game_id = rank_info['game_id']
        )
    # Add and commit the new game to the session
    db.session.add(rank)
    db.session.commit()
    # Send the new game back to the client
    return RankSchema().dump(rank), 201

# Read / get all ranks
@ranks_bp.route('/', methods=['GET'])
@jwt_required()
def all_users():
    admin_required()
    # Select * from rank;
    stmt = db.select(Rank).order_by(Rank.date_created)
    ranks = db.session.scalars(stmt).all()
    return RankSchema(many=True).dump(ranks)

# Read/Get one specific rank;
@ranks_bp.route('/<int:rank_id>', methods=['GET'])
@jwt_required()
def one_rank(rank_id):
    # Selecting the Rank, where the incoming game_id equals the id from the Model
    stmt = db.select(Rank).filter_by(rank_id=rank_id)
    rank = db.session.scalar(stmt)
    if rank:
        return RankSchema().dump(rank)
    else:
        return {'error': 'Rank not found'}, 404

@ranks_bp.route('/<int:rank_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_rank(rank_id):
    admin_required()
    stmt = db.select(Rank).filter_by(rank_id=rank_id)
    rank = db.session.scalar(stmt)
    rank_info = RankSchema().load(request.json)
    if rank:
        rank.rank = rank_info.get('rank', rank.rank)
        # Commit model changes to database
        db.session.commit()
        return RankSchema().dump(rank)
    else:
        return {'error': 'Rank not found'}, 404
    

@ranks_bp.route('/<int:rank_id>', methods=['DELETE'])
@jwt_required()
def delete_rank(rank_id):
    admin_required()
    stmt = db.select(Rank).filter_by(rank_id=rank_id)
    rank = db.session.scalar(stmt)
    if rank:
        db.session.delete(rank)
        db.session.commit()
        return {'message': 'The Rank has been deleted'}, 200
    else:
        return {'error': 'Rank not found'}, 404