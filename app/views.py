from flask import render_template, flash, redirect, request, session, url_for
from app import app
import time
from multiprocessing import Process
from LED_strip import strip, p, handler, light


@app.route('/')
@app.route('/index')
def index():
    # Initialize the library (must be called once before other functions).
    return render_template('index.html', title='Pixelate')

@app.route('/signal/<opcode>')
def signal(opcode):
    global p
    if (p.is_alive()):
        print "Killing process"
        p.terminate()

    handler.update_state(opcode)
    p = Process(target=send_signal, args=(opcode,))
    p.start()

    # return 0 from main in pixelate_send.cpp so anything non-zero
    # prolly means we encountered errors
    return redirect( url_for('index') )


def send_signal(opcode):
    handler.send(strip, light, opcode)
