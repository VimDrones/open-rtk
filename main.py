import serial
import socket                                         
import _thread
import time

import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

from luma.core.interface.serial import i2c, spi
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106

oled = sh1106(i2c(port=1, address=0x3C))

gnss_device = serial.Serial("/dev/serial0", 115200)

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = "0.0.0.0"                           

port = 1688                                           

# bind to the port
serversocket.bind((host, port))                                  

# queue up to 5 requests
serversocket.listen(5)                                           

current_client = None
def client_rx_thread():
    global current_client
    while True:
        if current_client:
            data = current_client.recv(1)
            gnss_device.write(data)

def client_tx_thread():
    global current_client
    while True:
        data = gnss_device.read(1)
        if current_client:
            current_client.send(data)

def gnss_thread():
    global current_client
    while True:
       # establish a connection
       clientsocket,addr = serversocket.accept()      
       print("Got a connection from %s" % str(addr))
       current_client = clientsocket

_thread.start_new_thread(client_tx_thread, ())
_thread.start_new_thread(client_rx_thread, ())
_thread.start_new_thread(gnss_thread, ())

width = oled.width
height = oled.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
padding = -2
top = padding
bottom = height - padding
x = 0
font = ImageFont.load_default()
while True:
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )

    # Write two lines of text.

    draw.text((x, top),       "IP: " + str(IP),  font=font, fill=255)
    draw.text((x, top+8),     str(CPU), font=font, fill=255)
    draw.text((x, top+16),    str(MemUsage),  font=font, fill=255)
    draw.text((x, top+25),    str(Disk),  font=font, fill=255)

    # Display image.
    oled.display(image)
    time.sleep(.1)
