class Handler(object):

    KITCHEN_MASK = 0x000F
    TV_WALL_MASK = 0x00F0
    COUCH_WALL_MASK = 0x0F00

    ON = 0x1
    OFF = 0x0

    THEATER_CHASE = 0x2
    RAINBOW = 0x4
    COLOR_WIPE = 0x8

    def __init__(self):
        pass

    def send(self, strip, opcode):
        print "Sending opcode: ", opcode
        op = int(opcode, 16)

        if (op & self.KITCHEN_MASK):
            op &= self.KITCHEN_MASK
            if (op == self.ON):
                print "Sending kitchen on"
                strip.on()

            elif (op == self.OFF):
                print "Sending kitchen off"
                strip.off()

            elif (op == self.THEATER_CHASE):
                print "Sending kitchen theater chase"
                while (True):
                    strip.theaterChase(strip.BRIGHT_WHITE)
                    strip.theaterChase(strip.RED)
                    strip.theaterChase(strip.BLUE)
                    strip.theaterChase(strip.GREEN)

            elif (op == self.RAINBOW):
                print "Sending kitchen rainbow"
                while (True):
                    strip.rainbow()

            elif (op == self.COLOR_WIPE):
                print "Sending kitchen color wipe"
                while (True):
                    strip.colorWipe(strip.BLUE)
                    strip.colorWipe(strip.RED)
                    strip.colorWipe(strip.GREEN)
                    strip.colorWipe(strip.BRIGHT_WHITE)

            else:
                print "Sending nothing atm"

        else:
            print "Sending off"
            strip.off()
