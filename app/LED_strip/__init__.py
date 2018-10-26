from multiprocessing import Process
p = Process()

from neopixel import *
from strip import Strip
from handler import Handler
from lifxled import MyLight

handler = Handler()
strip = Strip()
light = MyLight()
