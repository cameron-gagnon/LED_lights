from music_visualization.visualizer import Visualizer

class Handler(object):

    def __init__(self):
        self.visualizer = Visualizer()
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
            "drops": self.drops,
            "xmas": self.xmas,
            "lightning": self.lightning,
            "music": self.visualizer.start,
        }

        self.last_state = "off"
        self.cur_state = "off"

    def end(self):
        self.visualizer.stop()

    def send(self, strip, light, opcode):
        print "Sending opcode: ", opcode
        opcode = opcode.lower()
        if '-' in opcode:
            strip.rgbAlternateColors(opcode)
            light.sendOpcode(opcode)
        elif '|' in opcode:
            strip.rgbColor(opcode)
            light.sendOpcode(opcode)
        else:
            res = self.lookup.get(opcode, None)
            if res == None:
                light.sendInvalidOpcode()
                return
            light.sendOpcode(opcode)
            res(strip)

    def update_state(self, fn_name):
        self.last_state = self.cur_state
        if (fn_name == "toggle"):
            self.toggle_state()
        else:
            self.cur_state = fn_name

    def toggle_state(self):
        if (self.cur_state == "off"):
            self.cur_state = "toggle"
        else:
            self.cur_state = "off"

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

    def drops(self, strip):
        while(True):
            strip.drops()

    def lightning(self, strip):
        while(True):
            strip.lightning()

    def xmas(self, strip):
        strip.xmas()

    def on(self, strip):
        strip.on()

    def off(self, strip):
        strip.off()
