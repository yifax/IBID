# test BLE Scanning software
# jcs 6/8/2014

import blescan
import sys
import math

import bluetooth._bluetooth as bluez

dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	print "ble thread started"

except:
	print "error accessing bluetooth device..."
    	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

def helen(x,y,z):
	p = (x + y + z) / 2
	squ = abs(p*(p-x)*(p-y)*(p-z))
	return math.sqrt(squ)

rssi = ["","",""]
rssiv = [0,0,0]
counter = [0,0,0]
side = [0.0,0.0,0.0]
A = [62,62,68]

while ((counter[0]<5) or (counter[1]<3) or (counter[2]<3)):
	returnedList = blescan.parse_events(sock, 10)
	for beacon in returnedList:
		if ("dc:0d:30:4f:44:c7" in beacon):
			ibc = beacon.split(",")
			leng = len(ibc)
			rssi[2] = ibc[leng-1]
			rssiv[2] += int(rssi[2])
			counter[2] += 1
			print "No.2: " + rssi[2]
		elif ("dc:0d:30:4f:43:bf" in beacon):
			ibc = beacon.split(",")
			leng = len(ibc)
			rssi[0] = ibc[leng-1]
			rssiv[0] += int(rssi[0])
			counter[0] += 1
			print "No.0: " + rssi[0]
		elif ("dc:0d:30:4f:44:de" in beacon):
			ibc = beacon.split(",")
			leng = len(ibc)
			rssi[1] = ibc[leng-1]
			rssiv[1] += int(rssi[1])
			counter[1] += 1
			print "No.1: " + rssi[1]

n = 2.5
di = 3.0
gao = 3.0

for i in range(0,3):
	value = abs(rssiv[i] / counter[i])
	power = float((value - A[i]) / ( 10 * n ))
	d = pow(10 , power)
	if (i == 2):
		side[1] = d
	elif (i == 1):
		side[0] = d
	else: 
		side[2] = d
	print "iBeacon No." + str(i) + " intense= -" + str(value) + "db, distance = " + str(d)

x = helen(side[0],side[1],gao) * 2 / gao
y = helen(side[1],side[2],di) * 2 / di
print "(" + str(x) + "," + str(y) + ")"