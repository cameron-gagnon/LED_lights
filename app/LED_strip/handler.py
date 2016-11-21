class Handler(object):

    def __init__(self):
        self.lookup = {
            "on": self.on,
            "off": self.off,
            "mandb": self.m_and_b,
            "seizure": self.seizure,
            "chase": self.theater_chase,
            "gerald": self.gerald,
            "wipe": self.color_wipe,
            "cycle": self.cycle_all,
        }

    def send(self, strip, opcode):
        print "Sending opcode: ", opcode
        opcode = opcode.lower()
        res = self.lookup.get(opcode, self.off)
        res(strip)

    def theater_chase(self, strip):
        while(True):
            strip.full_theater_chase()

    def gerald(self, strip):
        while(True):
            strip.rainbow()

    def color_wipe(self, strip):
        while(True):
            strip.full_color_wipe()

    def m_and_b(self, strip):
        strip.maize_and_blue()

    def seizure(self, strip):
        while(True):
            strip.strobe()

    def cycle_all(self, strip):
        while(True):
            strip.cycle_all()

    def on(self, strip):
        strip.on()

    def off(self, strip):
        strip.off()

