from lifxlan import Light, BLUE, WHITE, WARM_WHITE, LifxLAN
import colorsys

class MyLight:
    OFF = False
    ON = True
    MAX = 65535
    MID = 65535/2
    CUSTOM_WHITE = WARM_WHITE[0], WARM_WHITE[1], WARM_WHITE[2]/2, WARM_WHITE[3]

    def __init__(self):
        self.light = None
        self.assignLight()

    def sendOpcode(self, opcode):
        # don't do anything
        return

        print("Got opcode", opcode)
        self.assignLight()
        if not self.light:
            return

        if opcode == "off":
            self.off()
            return

        #self.on()
        if '-' in opcode:
            rgbTuple = self.parseMultiColor(opcode)
            self.sendColor(rgbTuple)
        elif '|' in opcode:
            rgbTuple = self.parseSingleColor(opcode)
            self.sendColor(rgbTuple)

    def parseMultiColor(self, opcode):
        opcode1, opcode2 = opcode.split('-')
        return self.parseSingleColor(opcode1)

    def parseSingleColor(self, opcode):
        return opcode.split('|')

    def mapRange(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def sendColor(self, rgbTuple):
        self.light.set_power(self.ON, rapid=True)
        g, r, b = self.normalizeRGB(rgbTuple)
        print("Using g,r,b: '{},{},{}'".format(g,r,b))
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        print("Using hsv: '{},{},{}'".format(h,s,v))
        hHue = self.mapRange(h, 0, 1, 0, self.MAX)
        print("Using hHue: '{}'".format(hHue))
        self.light.set_hue(hHue, rapid=True)

    def normalizeRGB(self, rgbTuple):
        normalizedRGBs = []
        for val in rgbTuple:
            intVal = float(val)
            normalizedRGBs.append(self.mapRange(intVal, 0.0, 255.0, 0.0, 1.0))
        return normalizedRGBs

    def off(self):
        self.light.set_power(self.OFF, rapid=True)

    def on(self):
        print("Turning lifxlan on")
        self.light.set_power(self.ON, rapid=True)
        self.light.set_color(self.CUSTOM_WHITE, rapid=True)

    def warm(self):
        print("Warming up")
        self.light.set_power(self.ON, rapid=True)
        self.light.set_color(self.CUSTOM_WHITE, rapid=True)

    def sendInvalidOpcode(self):
        if not self.light:
            return
        self.light.set_color(WHITE, rapid=True)

    def assignLight(self):
        if not self.light:
            light = Light("d0:73:d5:26:30:b3","136.24.15.153")
            print("got light", light)
            if light:
                self.light = light
