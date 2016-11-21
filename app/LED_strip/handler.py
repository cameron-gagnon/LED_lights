class Handler(object):

    def __init__(self):
        pass

    def send(self, strip, opcode):
        print "Sending opcode: ", opcode
        opcode = opcode.lower()
        res = self.lookup.get(opcode, self.off)
        res()

    def theater_chase(self):
        while (True):
            strip.theaterChase(strip.BRIGHT_WHITE)
            strip.theaterChase(strip.RED)
            strip.theaterChase(strip.BLUE)
            strip.theaterChase(strip.GREEN)

    def gerald(self):
        while (True):
            strip.rainbow()

    def color_wipe(self):
        while (True):
            strip.colorWipe(strip.BLUE)
            strip.colorWipe(strip.RED)
            strip.colorWipe(strip.GREEN)
            strip.colorWipe(strip.BRIGHT_WHITE)

    def m_and_b(self):
        strip.custom({1: (0, 0, 255,),
                      2: (255,255,0,),
                      3: (0, 0, 255,),
                      4: (255,255,0,)})

    def seizure(self):
        while (True):
            strip.strobe()

    def on(self):
        strip.on()

    def off(self):
        strip.off()

    lookup = {
        "on": on,
        "off": off,
        "mandb": m_and_b,
        "seizure": seizure,
        "chase": theater_chase,
        "gerald": gerald,
        "wipe": color_wipe
    }
