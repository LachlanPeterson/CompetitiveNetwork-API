from init import db, ma
from marshmallow import fields, validates_schema
from marshmallow.validate import Length, And, Regexp, ValidationError

VALID_GENRES = ['Video Game', 'FPS', 'MOBA', 'MMO', 'RTS', 'Survival', 'Sports', 'Platforming']

class Game(db.Model):
   __tablename__ = 'games'

   game_id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(50))
   description = db.Column(db.Text())
   genre = db.Column(db.String(15))
   date_created = db.Column(db.Date())

   user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)

   user = db.relationship('User', back_populates='games')
   ranks = db.relationship('Rank', back_populates='game', cascade='all, delete')


class GameSchema(ma.Schema):
   user = fields.Nested('UserSchema', only=['name', 'email'])
   ranks = fields.List(fields.Nested('RankSchema', exclude=['game', 'rank_id']))
   title = fields.String(validate=And(
      Length(min=3, max=50),
      Regexp('^[a-zA-Z0-9 ]+$', error = 'Only letters, numbers and spaces are allowed')
      ))
   genre = fields.String(load_default=VALID_GENRES[0])

   @validates_schema()
   def validate_genre(self, data, **kwargs):
      genre = [x for x in VALID_GENRES if x.upper() == data['genre'].upper()]
      if len(genre) == 0:
         raise ValidationError(f'Genre must be one of: {VALID_GENRES}')
      
      data['genre'] = genre[0]

   class Meta:
      fields = ('game_id', 'title', 'description', 'genre', 'user', 'ranks')
      ordered = True
