from flask import render_template, flash, redirect, request, session, url_for, g
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db, lm
from .models import User
import time

@app.route('/')
@app.route('/index')
#@login_required
def index():
    user = g.user
    return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
#    if g.user is not None and g.user.is_authenticated:
#        return redirect(url_for('index'))
#
#    if request.method == 'POST':
#        session['remember_me'] = request.form.remember_me.data
#        flash('Login request for username="{}", remember_me={}'.format(
#               str(request.form['username']), str(form.remember_me.data)))
#        authenticate_user(request)
#        return redirect(request.args.get('next') or url_for('index'))
#
#    return render_template('login.html', title='Sign In', form=request.form)
    return redirect(url_for('index'))

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

def authenticate_user(request):
    user = User.query.filter_by(nickname = request.form.username.data).first()
    if user is None:
        nickname = request.form.username.data
        user = User(nickname = nickname)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if user == "cameron.gagnon@gmail.com":
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        login_user(user, remember = remember_me)
