from flask import render_template, flash, redirect, request
from app import app
from .forms import LoginForm
import time

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Cameron'}
    return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        flash('Login request for username="{}", remember_me={}'.format(
                form.username.data, str(form.remember_me.data)))
        return redirect('/index')

    return render_template('login.html', title='Sign In', form=form)
