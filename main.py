import serial
import socket                                         
import _thread
import time
import os
import subprocess
import psutil

import yaml
config_settings = yaml.load(open('./config.yml').read(), Loader=yaml.FullLoader)
gnss_port = config_settings['gnss_port']
gnss_port_baud = config_settings['gnss_port_baud']

from gnss_device.ublox import UBlox
ublox = UBlox(gnss_port, baudrate=gnss_port_baud, timeout=0.01)

dev = not socket.gethostname()=='raspberrypi'
from oled import Oled
oled = Oled(dev= dev)

def get_ip():
    global dev
    if dev:
        ip = list(map(int, socket.gethostbyname(socket.gethostname()).split("."))) 
    else:
        ip = list(map(int, subprocess.check_output("hostname -I", shell = True ).decode("utf-8").split("."))) 

    return ip

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

def gnss_proxy_thread():
    while True:
        if ublox.proxy:
            try:
                data = ublox.proxy.recv(1024)
            except Exception as e:
                ublox.proxy = None

            if data:
                ublox.write(data)
        else:
            # establish a connection
            clientsocket,addr = serversocket.accept()      
            print("Got a connection from %s" % str(addr))
            ublox.proxy = clientsocket

_thread.start_new_thread(gnss_proxy_thread, ())

def oled_thread():
    while True:
        cpu_usage = int(psutil.cpu_percent())
        mem = psutil.virtual_memory()
        memory_usage = int((mem.used / mem.total) * 100)
        oled.refresh(ublox.gnss_count, get_ip(), ublox.survey_in_acc, ublox.is_survey_in_success, cpu_usage, memory_usage)
        time.sleep(1)

_thread.start_new_thread(oled_thread, ())
_thread.start_new_thread(ublox.loop, ())

from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return 'OPEN BASE'

@app.route('/gnss')
def gnss():
    return jsonify(ublox.status)

app.run(host="0.0.0.0", port="3000")
