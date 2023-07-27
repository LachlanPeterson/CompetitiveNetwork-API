from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length

class User(db.Model):
  __tablename__ = 'users'

  user_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  email = db.Column(db.String(), nullable=False, unique=True)
  password = db.Column(db.String(), nullable=False)
  is_admin = db.Column(db.Boolean, default=False)
  date_created = db.Column(db.Date())

  games = db.relationship('Game', back_populates='user', cascade='all, delete')
  ranks = db.relationship('Rank', back_populates='user', cascade='all, delete')
  # games and ranks are both children from user as they are both foreign keys in the Class Game and Rank.
  # If the syncronized user is deleted, the children for that user will also be deleted.

# Marshmallow ma converts data types into DB readable format via the Schema and includes desired fields in JSON
class UserSchema(ma.Schema):
   games = fields.List(fields.Nested('GameSchema', exclude=['user', 'game_id']))
   ranks = fields.List(fields.Nested('RankSchema', exclude=['user', 'rank_id']))
   title = fields.String(validate=Length(min=3, max=50))
   # The UserSchema uses marshmallow to retrive the fields from both Game and Rank model via their individual Schemas.
   # The developer can choose what columns to exlcude or include from the models.

   class Meta:
      fields = ('user_id','name', 'email', 'password', 'date_created', 'is_admin', 'games', 'ranks')
      # fields Marshmallow function returns the chosen objects as JSON after the HTTP request