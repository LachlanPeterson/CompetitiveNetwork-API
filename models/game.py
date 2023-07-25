from init import db, ma

class Game(db.Model):
   __tablename__ = 'games'

   game_id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(50))
   description = db.Column(db.Text())
   genre = db.Column(db.String(50))
   rank_system = db.Column(db.Text())

# Marshmallow needs to know what fields to include in the Json
class GameSchema(ma.Schema):
   class Meta:
      fields = ('game_id', 'title', 'description', 'genre', 'rank_system')
      ordered = True