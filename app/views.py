from flask import render_template, flash, redirect, request, session, url_for
from app import app
import time
import subprocess


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Pixelate')

@app.route('/signal/<opcode>')
def signal(opcode):
    retCode = subprocess.call(['sudo', './pixelate_send', opcode])

    # return 0 from main in pixelate_send.cpp so anything non-zero
    # prolly means we encountered errors
    if retCode:
        print 'ERROR: exited with status: %d ' % retCode
    return redirect( url_for('index') )
