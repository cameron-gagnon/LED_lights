from music_visualization.visualizer import Visualizer
from helpers.decorators import loop
from strip import Strip
from lifxled import MyLight

class Handler():

    def __init__(self):
        self.strip = Strip()
        self.light = MyLight()
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
            "outrun": self.outrun,
        }

        self.last_state = "off"
        self.cur_state = "off"
        # noop function for initial effect on startup
        self.current_effect = lambda: None

    def run(self):
        while True:
            try:
                #print "Current effect is: '%s'" % self.current_effect
                self.current_effect()
            except KeyboardInterrupt:
                break

    def send(self, opcode):
        print "Sending opcode: ", opcode
        opcode = opcode.lower()
        if '-' in opcode:
            self.strip.rgbAlternateColors(opcode)
            self.light.sendOpcode(opcode)
        elif '|' in opcode:
            self.strip.rgbColor(opcode)
            self.light.sendOpcode(opcode)
        else:
            res = self.lookup.get(opcode, None)
            if res == None:
                self.light.sendInvalidOpcode()
                return
            self.light.sendOpcode(opcode)
            self.current_effect = res
            self.run()

    def update_state(self, fn_name):
        self.last_state = self.cur_state
        if (fn_name == "toggle"):
            self.toggle_state()
        else:
            self.cur_state = fn_name

        # end visualizer if the last state was music
        if self.last_state == "music":
            self.visualizer.stop()

    def toggle_state(self):
        if (self.cur_state == "off"):
            self.cur_state = "toggle"
        else:
            self.cur_state = "off"

    def theater_chase(self):
        self.strip.full_theater_chase()

    def gerald(self):
        self.strip.rainbow()

    def color_wipe(self):
        self.strip.full_color_wipe()

    def m_and_b(self):
        self.strip.maize_and_blue()

    def seizure(self):
        self.strip.strobe()

    def cycle_all(self):
        self.strip.cycle_all()

    def toggle(self):
        if self.last_state == "off":
            self.m_and_b()
        else:
            self.off()

    def drops(self):
        self.strip.drops()

    def lightning(self):
        self.strip.lightning()

    def xmas(self):
        self.strip.xmas()

    def on(self):
        self.strip.on()

    def off(self):
        self.strip.off()

    def outrun(self):
        self.strip.outrun()
