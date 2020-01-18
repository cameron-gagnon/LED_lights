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
* `sudo apt-get install scons python-dev swig python-scipy python-pyaudio`
* If pyaudio isn't fully installed, try installing:
  * sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
* `cd rpi_ws281x`
* `scons`
* Create file `/etc/modprobe.d/snd-blacklist.conf` with contents: `blacklist
  snd_bcm2835`. The rpi_ws281x library and Broadcom audio use PWM. This disables
  the driver so just the library uses PWN. See rpi_ws281x/README.md for more
  details.
* `cd python`
* `python2.7 ./setup.py build`
* `sudo python2.7 ./setup.py install`
* `sudo pip install lifxlan`
* Follow hardware config from here: https://github.com/scottlawsonbc/audio-reactive-led-strip
