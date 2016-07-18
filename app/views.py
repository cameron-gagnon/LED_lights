from flask import render_template, flash, redirect, request, session, url_for
from app import app
import time

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Pixelate')
