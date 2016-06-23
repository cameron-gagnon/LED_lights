from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

# putting this import after the `app = Flask(__name__)` line prevents
# circular imports
from app import views, models
