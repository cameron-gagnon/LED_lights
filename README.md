Pixelated
===

## Features ##

* Decent interface on mobile and web
* Uses AJAX requests so the main webpage does not reload
* Many patterns can be pre-programmed and sent on the fly

## TODO ##
* Add hardware list, setup process, and overall description here for others to use. Contact me if you would like information on this


Steps to re-install this repo:
* use python2.7 (even tho it's old and out of date)
* clone repo
* `sudo apt-get install scons`
* `cd rpi_ws281x`
* `scons`
* `cd python`
* `sudo apt-get install python-dev swig`
* `python2.7 ./setup.py build`
* `python2.7 ./setup.py install`
* `sudo pip install lifxlan`
