from lifxlan import Light, BLUE
import colorsys

class MyLight:
    OFF = 0
    MAX = 65535
    def __init__(self):
        self.light = Light("d0:73:d5:26:30:b3", "192.168.128.14")

    def sendOpcode(self, opcode):
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
        g, r, b = self.normalizeRGB(rgbTuple)
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        hHue = self.mapRange(h, 0, 1, 0, self.MAX)
        self.light.set_color([hHue, self.MAX, self.MAX, 3500])

    def normalizeRGB(self, rgbTuple):
        normalizedRGBs = []
        for val in rgbTuple:
            intVal = float(val)
            normalizedRGBs.append(self.mapRange(intVal, 0.0, 255.0, 0.0, 1.0))
        return normalizedRGBs

    def off(self):
        self.light.set_power(self.OFF)

    def sendInvalidOpcode(self):
        self.light.set_color(BLUE)
