from init import db, ma
from marshmallow import fields

class Rank(db.Model):
   __tablename__ = 'ranks'

   rank_id = db.Column(db.Integer, primary_key=True)

   rank = db.Column(db.String(50))
   date_created = db.Column(db.Date())

   user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
   user = db.relationship('User', back_populates='ranks')

   game_id = db.Column(db.Integer, db.ForeignKey('games.game_id', ondelete='CASCADE'), nullable=False)
   game = db.relationship('Game', back_populates='ranks')


class RankSchema(ma.Schema):
   user = fields.Nested('UserSchema', only=['name', 'email'])
   game = fields.Nested('GameSchema', only=['title', 'genre', 'rank_system'])

   class Meta:
      fields = ('rank_id', 'rank', 'date_created', 'user', 'game')
      ordered = True
