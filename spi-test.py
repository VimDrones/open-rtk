import time
import sys
import spidev

spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 0b11
spi.max_speed_hz = 125000
while True:
    for i in range(100):
        spi.xfer(i)
    time.sleep(0.01)
