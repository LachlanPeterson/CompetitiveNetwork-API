from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# protocol + adapter + username and password @ the port
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://cn_dev:cndev123@localhost:5432'

# Must be after config

# Open connection to database
db = SQLAlchemy(app)
print(db.__dict__)

@app.route('/')
def index():
    return 'Competitive Rank Review Home'

if __name__ == '__main__':
    app.run(debug=True)