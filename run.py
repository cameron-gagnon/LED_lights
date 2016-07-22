#! /usr/bin/env python2.7
from app import app
import sys

def getPort():
    port = 80
    if len(sys.argv) > 1:
        port = sys.argv[1]
    return int(port)


app.run(debug=True, host='0.0.0.0', port = getPort())
