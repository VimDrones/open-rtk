import time
import sys
import spidev

spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 0b11
spi.max_speed_hz = 125000 * 16

import struct
HEADER = 0xAA
END = 0x55

gnss_count = 14
ip = [192,168,1,100]
acc = 2 
survey_in = False
cpu_usage = 80
memory_usage = 60
empty = 0

while True:
    for i in range(100):
        gnss_count = i
    data = struct.pack('B B BBBB I B B B B B', HEADER, gnss_count, ip[0], ip[1], ip[2], ip[3], acc, survey_in, cpu_usage, memory_usage, empty, END)
    spi.xfer(data)
    time.sleep(0.2)
