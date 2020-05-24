from flask import render_template, redirect, url_for, jsonify
from app import app
from multiprocessing import Process

from LED_strip import handler
p = Process()

@app.route('/')
@app.route('/index')
def index():
    # Initialize the library (must be called once before other functions).
    settings = handler.settings()
    return render_template('index.html', title='Pixelate', settings=settings['settings'])

@app.route('/signal/<opcode>')
def signal(opcode):
    global p

    handler.update_state(opcode)

    if (p.is_alive()):
        print "Killing process"
        p.terminate()

    p = Process(target=send_signal, args=(opcode,))
    p.start()

    # return 0 from main in pixelate_send.cpp so anything non-zero
    # prolly means we encountered errors
    return redirect( url_for('index') )


# API endpoint to return available colors to set
@app.route('/settings')
def settings():
    return jsonify(handler.settings())
def send_signal(opcode):
    handler.send(opcode)
