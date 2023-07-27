from init import db, ma
from marshmallow import fields, validates_schema
from marshmallow.validate import ValidationError

VALID_RANKS = ['Unranked', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Master']

class Rank(db.Model):
   __tablename__ = 'ranks'

   rank_id = db.Column(db.Integer, primary_key=True)
   rank = db.Column(db.String())
   date_created = db.Column(db.Date())

   user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
   game_id = db.Column(db.Integer, db.ForeignKey('games.game_id', ondelete='CASCADE'), nullable=False)
   
   user = db.relationship('User', back_populates='ranks')
   game = db.relationship('Game', back_populates='ranks')

class RankSchema(ma.Schema):
   user = fields.Nested('UserSchema', only=['name', 'email'])
   game = fields.Nested('GameSchema', only=['title', 'genre'])
   rank = fields.String(load_default=VALID_RANKS[0])

   @validates_schema()
   def validate_genre(self, data, **kwargs):
      rank = [x for x in VALID_RANKS if x.upper() == data['rank'].upper()]
      if len(rank) == 0:
         raise ValidationError(f'Ranks must be one of: {VALID_RANKS}')
      
      data['rank'] = rank[0]

   class Meta:
      fields = ('rank_id', 'rank', 'date_created', 'user', 'game')
      ordered = True
