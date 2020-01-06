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
        
    def refresh(self, gnss_count, ip, acc, survey_in, cpu_usage, memory_usage, empty1=0, empty2=0):
        if acc > 4294967295:
            acc = 4294967295

        data = struct.pack('<B B BBBB I B B B B B B', HEADER, gnss_count, *ip, acc, survey_in, cpu_usage, memory_usage, empty1, empty2, END)
        if not self.dev:
            self.spi.xfer(data)

        print(struct.unpack('<B B BBBB I B B B B B B', data)
        if False:
            print("ublox.gps_count", gnss_count)
            print("ublox.is_survey_in_success", survey_in)
            print("ublox.survey_in_acc", acc)
            print("host_ip", ip)
            print("cpu_usage", cpu_usage)
            print("memory_usage", memory_usage)
            print(len(data))
