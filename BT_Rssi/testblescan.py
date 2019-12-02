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
	return math.sqrt(p*(p-a)*(p-b)*(p-c))

rssi = ["","",""]
rssiv = [0,0,0]
counter = [0,0,0]
side = [0.0,0.0,0.0]

while ((counter[0]<3) or (counter[1]<3) or (counter[2]<3)):
	returnedList = blescan.parse_events(sock, 10)
	for beacon in returnedList:
		if ("dc:0d:30:4f:44:c7" in beacon):
			ibc = beacon.split(",")
			leng = len(ibc)
			rssi[2] = ibc[leng-1]
			rssiv[2] += int(rssi[2])
			counter[2] += 1
		elif ("c2:93:3e:1c:65:d4" in beacon):
			ibc = beacon.split(",")
			leng = len(ibc)
			rssi[0] = ibc[leng-1]
			rssiv[0] += int(rssi[0])
			counter[0] += 1
		elif ("d7:f0:62:93:92:63" in beacon):
			ibc = beacon.split(",")
			leng = len(ibc)
			rssi[1] = ibc[leng-1]
			rssiv[1] += int(rssi[1])
			counter[1] += 1

A = 38.0	# Need test
n = 27.0
di = ?
gao = ?

for i in range(0,3):
	value = abs(rssiv[i] / counter[i])
	power = float((value - A) / ( 10 * n ))
	d = pow(10 , power)
	side[0] = d
	print "iBeacon No." + str(i) + " intense= -" + str(value) + "db, distance = " + str(d)[0:5]


x = helen(side[0],side[1],di)
y = helen(side[1],side[2],gao)