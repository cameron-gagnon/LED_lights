import os
from flask import Flask

app = Flask(__name__)

# putting this import after the `app = Flask(__name__)` line prevents
# circular imports
from app import views
