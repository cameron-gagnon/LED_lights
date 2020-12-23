#!/usr/bin/env python2.7

import time
import random
from neopixel import *

class Strip(object):
    # LED self.strip configuration:
    LED_COUNT      = 300     # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 155     # Set to 0 for darkest and 255 for brightest
    MAX_COLOR      = 255
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    RANGE          = 40      # range to be used in spread function

    WHITE = Color(40,40,40) # can't go full brightness otherwise color distortion happens
    BRIGHT_WHITE = Color(100,100,100) # for use when not all of the strand will be on
    OFF = Color(0,0,0)
    GREEN = Color(255,0,0)
    RED = Color(0,255,0)
    BLUE = Color(0,0,255)
    YELLOW = Color(127,127,0)
    DIM_YELLOW = Color(80,80,0)
    ORANGE = Color(35,255,0)

    MAX_LIGHTNING_SLEEP = 5000

    def __init__(self):
        # only functions that are mapped here should be called externally
        self._settings = {
            "on"       : self.on,
            "off"      : self.off,
            "wipe"     : self.full_wipe,
            "uofm"     : self.maize_and_blue,
            "xmas"     : self.xmas,
            "chase"    : self.full_chase,
            "cycle"    : self.cycle_all,
            "drops"    : self.drops,
            "strobe"   : self.strobe,
            "outrun"   : self.outrun,
            "gerald"   : self.rainbow,
            "rainbow"  : self.rainbowCycle,
            "lightning": self.lightning,
            "airheads" : self.airheads,
        }

        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN,
                                   self.LED_FREQ_HZ, self.LED_DMA,
                                   self.LED_INVERT, self.LED_BRIGHTNESS)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    def get_settings(self):
        return self._settings.keys()

    def get_fn(self, opcode):
        if not opcode:
            return lambda: None

        return self._settings.get(opcode.lower(), lambda: None)

    # Define functions which animate LEDs in various ways.
    def wipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def chase(self, color, wait_ms=50, iterations=10):
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
        pos %= self.MAX_COLOR
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
                self.strip.setPixelColor(i, self.wheel(i+j))
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def rainbowCycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i * 256 / self.strip.numPixels()) + j))

            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(self.MAX_COLOR+1):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, self.wheel(i+j))

                self.strip.show()
                time.sleep(wait_ms/1000.0)

                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, 0)

    def strobe(self, color=WHITE, delay=50):

        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)

        self.strip.show()
        time.sleep(delay/1000.0)

        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, self.OFF)

        self.strip.show()
        time.sleep(delay/1000.0)

    def full_wipe(self):
        self.wipe(self.BLUE)
        self.wipe(self.DIM_YELLOW)
        self.wipe(self.RED)
        self.wipe(self.GREEN)
        self.wipe(self.WHITE)

    def full_chase(self):
        self.chase(self.BRIGHT_WHITE)
        self.chase(self.RED)
        self.chase(self.BLUE)
        self.chase(self.YELLOW)
        self.chase(self.GREEN)

    def maize_and_blue(self):
        self.alternate_colors(self.BLUE, self.YELLOW)

    def cycle_all(self):
        # cycles through each pattern for a little bit (except strobe)
        DURATION = 10 # seconds
        self.full_wipe()
        self.full_theater_chase()
        self.rainbow()
        self.maize_and_blue()
        time.sleep(DURATION)
        self.on()
        time.sleep(DURATION)

    def drops(self):
#        for i in range(self.strip.numPixels()):
#            self.strip.setPixelColor(i, self.WHITE)

        one_strip_len = int(self.strip.numPixels()/2)
        for i in range(one_strip_len):
            for j in range(one_strip_len, i, -1):
                self.strip.setPixelColor(j, self.WHITE)
                self.strip.setPixelColor(j+one_strip_len, self.WHITE)
                self.strip.show()
                self.strip.setPixelColor(j, self.OFF)
                self.strip.setPixelColor(j+one_strip_len, self.OFF)

            self.strip.setPixelColor(i, self.WHITE)
            self.strip.setPixelColor(i+one_strip_len, self.WHITE)
            self.strip.show()

    def xmas(self):
        self.alternate_colors(self.GREEN, self.RED)

    def alternate_colors(self, color1, color2):
        cur_color = color1
        ALTERNATING_AMOUNT = 10
        counter = 0

        for i in range(self.strip.numPixels()):
            # change values from maize to blue every 10 pixels
            if counter >= ALTERNATING_AMOUNT:
                cur_color = color1 if cur_color == color2 else color2
                counter = 0

            counter += 1

            self.strip.setPixelColor(i, cur_color)

        self.strip.show()

    def on(self):
        self._steady(self.WHITE)

    def off(self):
        self._steady(self.OFF)

    def lightning(self):
        color = Color(186,85,211)
        fn_and_args = random.choice([[self._spread, color, 15, 3],
                [self.strobe, color, 40, 5], [self._streak, color, 0.01, 1]])
        fn = fn_and_args[0]
        args = fn_and_args[1:-1]
        num_times = fn_and_args[-1]
        delay = fn_and_args[2]

        for i in range(random.randint(0,num_times)):
            fn(*args)

        sleep_amt = random.randint(10, self.MAX_LIGHTNING_SLEEP)
        time.sleep(sleep_amt/1000)

    def airheads(self, wait_ms=35, airhead_strip_len=20):
        """Draw a repeated airheads pattern that moves across the whole strand"""
        for j in range(airhead_strip_len):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self._airHeadStrip(i+j, airhead_strip_len))
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def _airHeadStrip(self, pos, airhead_strip_len):
        pos %= airhead_strip_len
        pos_to_strip_color = [
            (1, self.GREEN),
            (2, self.BLUE),
            (3, self.DIM_YELLOW),
            (4, self.ORANGE),
            (5, self.RED),
        ]
        num_buckets = len(pos_to_strip_color)
        for bucket_num, color in pos_to_strip_color:
            if pos < airhead_strip_len/num_buckets * bucket_num:
                return color

    def outrun(self):
        # we really want the midpoint of the visible strands, not the technical
        # midpoint. This number will change as the setup changes
        MIDPOINT = 78
        # how drastic the color changes between changes
        STEP = 1
        # blanks/black lines occur at these values to imitate the lines in the
        # outrun sun
        blanks = [42, 48, 49, 50, 55, 56, 57, 58, 59, 63, 64, 65, 66, 67, 68, 69]
        base_brightness = 80

        for i in range(self.LED_COUNT/2):
            pos_offset = MIDPOINT + i
            neg_offset = MIDPOINT - i

            if i in blanks:
                color = self.OFF
            else:
                color = Color(max(base_brightness - (i*STEP), 0),
                              min(base_brightness + (i*STEP), 255),
                              0)

            self.strip.setPixelColor(pos_offset, color)
            self.strip.setPixelColor(neg_offset, color)

        self.strip.show()

  # ==== PRIVATE ====
  # shouldn't be called externally

    def _steady(self, color):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)

        self.strip.show()

    def _spread(self, color=WHITE, delay=15):
        strike_pos = random.randint(self.RANGE, self.strip.numPixels() - self.RANGE)
        self.strip.setPixelColor(strike_pos, color)
        self.strip.show()
        self.strip.setPixelColor(strike_pos, self.OFF)

        for i in range(self.RANGE):
            self.strip.setPixelColor(strike_pos + i, color)
            self.strip.setPixelColor(strike_pos - i, color)
            self.strip.show()
            time.sleep(delay/1000)
            self.strip.setPixelColor(strike_pos + i - 2, self.OFF)
            self.strip.setPixelColor(strike_pos - i + 2, self.OFF)

        self.off()

    def _rgbColor(self, rgbColor):
        r, g, b = self._split(rgbColor, '|')
        print('red', r, 'green', g, 'blue', b)
        self._steady(Color(int(r), int(g), int(b)))

    def _rgbAlternateColors(self, colors):
        color1, color2 = self._split(colors, '-')
        r1, g1, b1 = self._split(color1, '|')
        r2, g2, b2 = self._split(color2, '|')
        self.alternate_colors(Color(int(r1),int(g1),int(b1)),
                              Color(int(r2),int(g2),int(b2)))

    def _split(self, color, symbol):
        return color.split(symbol)

    def _streak(self, color, delay=0.5):
        offset = random.randint(self.RANGE, self.strip.numPixels() - self.RANGE)
        offset2 = random.randint(self.RANGE, self.strip.numPixels() - self.RANGE)
        pos = [offset, offset2]
        pos.sort()
        for i in range(pos[0], pos[1], 3):
            self.strip.setPixelColor(i, color)
            self.strip.setPixelColor(i+1, color)
            self.strip.setPixelColor(i+2, color)
            self.strip.show()
            time.sleep(delay/1000.0)

        self.off()


if __name__ == "__main__":
    s = Strip()
    print "Press Ctrl-C to quit"
    try:
        while True:
            s.rainbowCycle()
    except KeyboardInterrupt:
        print "Closing"
