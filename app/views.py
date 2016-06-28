from flask import render_template, flash, redirect, request, session, url_for
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db, lm
from .models import User
import time

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Pixelate')
