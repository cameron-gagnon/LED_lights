from flask import render_template, flash, redirect, request, session, url_for, g
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db, lm
from .forms import LoginForm
from .models import User
import time

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        session['remember_me'] = form.remember_me.data
        flash('Login request for username="{}", remember_me={}'.format(
                form.username.data, str(form.remember_me.data)))
        authenticate_user(form)
        return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

def authenticate_user(form):
    user = User.query.filter_by(nickname = form.username.data).first()
    if user is None:
        nickname = form.username.data
        user = User(nickname = nickname)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
