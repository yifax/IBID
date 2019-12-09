import serial
import time
port = serial.Serial("/dev/rfcomm0", baudrate=9600)
 
# Use this code to test BT communication between Arduino Car and Raspberry Pi Car
while True:
	print "SENDING..."
	port.write(str(3))
	rcv = port.readline()
	if rcv:
	   print(rcv)