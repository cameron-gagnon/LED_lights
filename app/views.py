from flask import render_template, flash, redirect, request, session, url_for
from app import app
import time

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Pixelate')

@app.route('/sendsignal/<signal>', methods=['POST'])
def send_signal(signal):
    print 'Sending signal: %d ' % (signal)

    retCode = subprocess.call(['./pixelated', signal])

    if not retCode:
        print 'ERROR: exited with status: %d ' % retCode
