import time
import sys

import struct
HEADER = 0xAA
END = 0x55

#  gnss_count = 14
#  ip = [192,168,1,100]
#  acc = 2 
#  survey_in = False
#  cpu_usage = 80
#  memory_usage = 60
#  empty = 0

class Oled(object):

    def __init__(self, dev=False):
        self.dev = dev
        if not self.dev:
            import spidev
            self.spi = spidev.SpiDev()
            self.spi.open(0,0)
            self.spi.mode = 0b11
            self.spi.max_speed_hz = 125000 * 16
        
    def refresh(self, gnss_count, ip, acc, survey_in, cpu_usage, memory_usage, empty):
        data = struct.pack('<B B BBBB I B B B B B', HEADER, gnss_count, *ip, acc, survey_in, cpu_usage, memory_usage, empty, END)
        if not self.dev:
            self.spi.xfer(data)
        else:
            print(len(data))
