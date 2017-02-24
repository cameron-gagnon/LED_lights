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
            "toggle": self.toggle,
        }

        # default to off as the last state
        self.last_state = "off"

    def send(self, strip, opcode):
        print "Sending opcode: ", opcode
        opcode = opcode.lower()
        res = self.lookup.get(opcode, self.off)

        res(strip)

        # this happens after calling the opcode function
        # because when we call the "toggle" function
        # it uses the last_state value, so we don't
        # want to update the last_state before we use it
        set_last_state(res)

    def set_last_state(self, fn_name):
        if (fn_name == "toggle"):
            toggle_last_state()
        else:
            self.last_state = fn_name

    def toggle_last_state(self):
        if (self.last_state == "off"):
            self.last_state == "toggle"
        else:
            self.last_state == "off"

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

    def toggle(self, strip):
        if self.last_state == "off":
            self.m_and_b(strip)
        else:
            self.off(strip)

    def on(self, strip):
        strip.on()

    def off(self, strip):
        strip.off()
