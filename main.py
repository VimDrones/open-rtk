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

from oled import Oled
oled = Oled()

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
        host_ip = socket.gethostbyname(socket.gethostname())
        cpu_usage = int(psutil.cpu_percent())
        mem = psutil.virtual_memory()
        memory_usage = int((mem.used / mem.total) * 100)
        if True:
            print("ublox.gps_count", ublox.gnss_count)
            print("ublox.is_survey_in_success", ublox.is_survey_in_success)
            print("ublox.survey_in_acc", ublox.survey_in_acc)
            print("host_ip", host_ip)
            print("cpu_usage", cpu_usage)
            print("memory_usage", memory_usage)
        oled.refresh(ublox.gnss_count, host_ip, ublox.survey_in_acc, ublox.is_survey_in_success, cpu_usage, memory_usage, 0)
        time.sleep(0.2)

_thread.start_new_thread(oled_thread, ())

ublox.loop()

serversocket.close()
