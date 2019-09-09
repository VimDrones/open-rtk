import serial
import socket                                         
import _thread

gnss_device = serial.Serial("/dev/serial0", 115200)

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           

port = 9999                                           

# bind to the port
serversocket.bind((host, port))                                  

# queue up to 5 requests
serversocket.listen(5)                                           

current_client = None
def client_rx_thread():
    global current_client
    while True:
        if current_client:
            data = current_client.recv(1024)
            print("tx:", data)
            gnss_device.write(data)
            print(data)

def client_tx_thread():
    global current_client
    while True:
        data = gnss_device.read(1024)
        print("rx:", data)
        if current_client:
            current_client.send(data)

_thread.start_new_thread(client_tx_thread, ())
_thread.start_new_thread(client_rx_thread, ())

while True:
   # establish a connection
   clientsocket,addr = serversocket.accept()      
   print("Got a connection from %s" % str(addr))
   current_client = clientsocket
