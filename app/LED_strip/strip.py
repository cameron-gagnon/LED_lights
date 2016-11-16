#!/usr/bin/env python2.7

import time
from neopixel import *

class Strip(object):
    # LED self.strip configuration:
    LED_COUNT      = 150      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


    WHITE = Color(40,40,40) # can't go full brightness otherwise color distortion happens
    BRIGHT_WHITE = Color(100,100,100) # for use when not all of the strand will be on
    OFF = Color(0,0,0)
    RED = Color(255,0,0)
    GREEN = Color(0,255,0)
    BLUE = Color(0,0,255)

    def __init__(self):
        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN,
                                   self.LED_FREQ_HZ, self.LED_DMA,
                                   self.LED_INVERT, self.LED_BRIGHTNESS)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    # Define functions which animate LEDs in various ways.
    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def theaterChase(self, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, color)

                self.strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, 0)

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i+j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def rainbowCycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel(((i * 256 / self.strip.numPixels()) + j) & 255))

            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, self.wheel((i+j) % 255))

                self.strip.show()
                time.sleep(wait_ms/1000.0)

                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, 0)

    def steady(self, color):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)

        self.strip.show()

    def on(self):
        self.steady(self.WHITE)

    def off(self):
        self.steady(self.OFF)

if __name__ == "__main__":
    s = Strip()
    print "Press Ctrl-C to quit"
    try:
        while True:
            s.rainbowCycle()
#        while True:
#            s.on()
#            time.sleep(1)
#            s.off()
#            time.sleep(1)
#            s.on()
#            time.sleep(1)
#            s.off()
#            time.sleep(1)
#            s.colorWipe(s.WHITE)
#            s.colorWipe(s.RED)
#            # Color wipe animations.
#            s.colorWipe(s.RED)  # Red wipe
#            s.colorWipe(s.BLUE)  # Blue wipe
#            s.colorWipe(s.GREEN)  # Green wipe
#            # Theater chase animations.
#            s.theaterChase(Color(127, 127, 127))  # White theater chase
#            s.theaterChase(Color(127,   0,   0))  # Red theater chase
#            s.theaterChase(Color(  0,   0, 127))  # Blue theater chase
#            # Rainbow animations.
#            s.rainbow()
#            s.rainbowCycle()
#            s.theaterChaseRainbow()
    except KeyboardInterrupt:
        print "Closing"
