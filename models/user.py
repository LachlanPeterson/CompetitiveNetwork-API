from init import db, ma

# User Entity model for Users
class User(db.Model):
  __tablename__ = 'users'

  user_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50)) # name 16 characters max
  email = db.Column(db.String(50), nullable=False, unique=True)
  password = db.Column(db.String(), nullable=False)
  is_admin = db.Column(db.Boolean, default=False)
  date_created = db.Column(db.Date())

class UserSchema(ma.Schema):
   class Meta:
      fields = ('name', 'email', 'password', 'date_created', 'is_admin')