from music_visualization.visualizer import Visualizer
from helpers.decorators import loop
from strip import Strip
from lifxled import MyLight

class Handler():

    def __init__(self):
        self.strip = Strip()
        self.light = MyLight()
        self.visualizer = Visualizer()
        self._settings = {
            "music": self.visualizer.start,
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

    def settings(self):
        strip_settings = self.strip.get_settings()
        handler_settings = self._settings.keys()
        print("strip_settings:", strip_settings)
        print("handler_settings:", handler_settings)

        json_settings = {
            "settings": strip_settings + handler_settings
        }
        return json_settings

    def send(self, opcode):
        print "Sending opcode: ", opcode
        opcode = opcode.lower()
        if '-' in opcode:
            self.strip._rgbAlternateColors(opcode)
            self.light.sendOpcode(opcode)
        elif '|' in opcode:
            self.strip._rgbColor(opcode)
            self.light.sendOpcode(opcode)
        else:
            effect = self._get_fn(opcode) or self.strip.get_fn(opcode)
            self.current_effect = effect
            self.run()

    def _get_fn(self, opcode):
        return self._settings.get(opcode.lower())

    def update_state(self, fn_name):
        # end visualizer if the last state was music
        if self.cur_state == "music":
            self.visualizer.stop()

        self.last_state = self.cur_state
        self.cur_state = fn_name
