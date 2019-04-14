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
        print("Got opcode")
        self.assignLight()
        #if not self.light:
        #    return
        #if '-' in opcode:
        #    rgbTuple = self.parseMultiColor(opcode)
        #    self.sendColor(rgbTuple)
        #elif '|' in opcode:
        #    rgbTuple = self.parseSingleColor(opcode)
        #    self.sendColor(rgbTuple)
        if opcode == "off":
            self.off()
        else:
            pass
            #self.warm()

    def parseMultiColor(self, opcode):
        opcode1, opcode2 = opcode.split('-')
        return self.parseSingleColor(opcode1)

    def parseSingleColor(self, opcode):
        return opcode.split('|')

    def mapRange(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def sendColor(self, rgbTuple):
        g, r, b = self.normalizeRGB(rgbTuple)
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        hHue = self.mapRange(h, 0, 1, 0, self.MAX)
        self.light.set_color(WARM_WHITE, rapid=True)

    def normalizeRGB(self, rgbTuple):
        normalizedRGBs = []
        for val in rgbTuple:
            intVal = float(val)
            normalizedRGBs.append(self.mapRange(intVal, 0.0, 255.0, 0.0, 1.0))
        return normalizedRGBs

    def off(self):
        self.light.set_power(self.OFF, rapid=True)

    def on(self):
        self.light.set_color(self.CUSTOM_WHITE, rapid=True)
        self.light.set_power(self.ON, rapid=True)

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
            light = LifxLAN(1).get_lights()
            if len(light) > 0:
                self.light = light[0]
