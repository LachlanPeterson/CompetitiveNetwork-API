from flask import Blueprint, request
from models.rank import Rank, RankSchema
from init import db
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required, admin_or_owner_required

ranks_bp = Blueprint('ranks', __name__, url_prefix='/ranks')

# Read all users
@ranks_bp.route('/', methods=['GET'])
@jwt_required()
def all_users():
    admin_required()
    # Select * from rank;
    stmt = db.select(Rank).order_by(Rank.user_id)
    ranks = db.session.scalars(stmt).all()
    return RankSchema(many=True).dump(ranks)

