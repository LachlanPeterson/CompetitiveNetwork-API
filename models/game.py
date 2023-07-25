from init import db, ma
from marshmallow import fields

class Game(db.Model):
   __tablename__ = 'games'

   game_id = db.Column(db.Integer, primary_key=True)

   title = db.Column(db.String(50))
   description = db.Column(db.Text())
   genre = db.Column(db.String(50))
   rank_system = db.Column(db.Text())
   date_created = db.Column(db.Date())

   user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
   user = db.relationship('User', back_populates='games')
   ranks = db.relationship('Rank', back_populates='game')


# Marshmallow needs to know what fields to include in the Json
class GameSchema(ma.Schema):
   # Telling marshmallow to use UserSchema to serialize the 'user' field
   user = fields.Nested('UserSchema', exclude=['password', 'date_created', 'games'])
   ranks = fields.List(fields.Nested('RankSchema', exclude=['game', 'rank_id']))

   class Meta:
      fields = ('game_id', 'title', 'description', 'genre', 'rank_system', 'user', 'ranks')
      ordered = True
