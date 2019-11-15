import serial
gnss_device = serial.Serial("/dev/serial0", 115200)

print("gnss serial0 testing, baud 115200 ....")
while True:
    data = gnss_device.read(1024)
    if data:
        print(data)

    gnss_device.write(b'TX OK')
