import blescan
import sys
import math
import bluetooth._bluetooth as bluez
import logging
import os

from flask import Flask
from flask_ask import Ask, request, session, question, statement
import RPi.GPIO as GPIO
import time, math
from time import sleep
import serial
import sys

port = serial.Serial("/dev/rfcomm0", baudrate=9600) # necessary env sitting for BT communication
address = 0x48	# default address of PCF8591(A/D)
channel = 0x40  # address for A0 on PCF8591


in1 = 22
in2 = 23
in3 = 24
in4 = 25

ena = 20
enb = 21

speedr = 7
speedl = 8

temp1 = 1

start_timer_left = time.time()
start_timer_right = time.time()
rpml = 0
rpmr = 0
pulser = 0
pulsel = 0
elapsel = 0
elapser = 0

echor = 27
trigr = 17
echol = 26
trigl = 19
trigw = 10
echow = 9
trigf = 5
echof = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(ena, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)
GPIO.setup(echor, GPIO.IN)
GPIO.setup(echol, GPIO.IN)
GPIO.setup(echow, GPIO.IN)
GPIO.setup(echof, GPIO.IN)
GPIO.setup(trigl, GPIO.OUT)
GPIO.setup(trigr, GPIO.OUT)
GPIO.setup(trigw, GPIO.OUT)
GPIO.setup(trigf, GPIO.OUT)

GPIO.setup(speedl, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(speedr, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

p1 = GPIO.PWM(ena, 100)  
p2 = GPIO.PWM(enb, 100)  
p1.start(20)     # Right
p2.start(20)     # Left

pwml = 15
pwmr = 16

inital_wall_dis = 20
inital_front_dis = 20
inital_diff = 0


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

PAUSE = ['pause','stop']
FORWARD = ['forward','front']
BACKWARD = ['backward','back']
RIGHT = ['right']
LEFT = ['left']
MASTER = ['master']
SLAVE = ['slave']


# Indoor Positioning System
def helen(x,y,z):
	p = (x + y + z) / 2
	squ = abs(p*(p-x)*(p-y)*(p-z))
	return math.sqrt(squ)

def rssi():
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
    coor = [x,y]
    return coor

def locating():
    coor = rssi()
    if ((coor[0] > 1.5) and (oor[0] > 1.5)):
        turn_left(1.5)
    elif ((coor[0] < 1.5) and (oor[0] < 1.5)):
        turn_right(1.5)
    elif ((coor[0] < 1.5) and (oor[0] > 1.5)):
        turn_left(0.75)
    elif ((coor[0] > 1.5) and (oor[0] < 1.5)):
        turn_right(0.75)

# Master Operation
def forward():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)

def backward():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)

def pause():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

def turn_left(angle):
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    sleep(angle)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

def turn_right(angle):
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    sleep(angle)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

# Slave Operation
def bluet(message):
    port.flushInput()
    if (message == 1) :
        port.write(bytes('f','utf-8'))
        print("command sent: run")

    elif (message == 0) :
        port.write(bytes('s','utf-8'))
        print("command sent: stop")

    elif (message == 4) :
        port.write(bytes('b','utf-8'))
        print("command sent: back")
    
    elif (message == 2) :
        port.write(bytes('r','utf-8'))
        print("command sent: turn left")
    
    elif (message == 3) :
        port.write(bytes('l','utf-8'))
        print("command sent: turn right")

# Sensors System
def get_ultra(port):
    
    if (port == 0): 
        trig = trigl
        echo = echol
    elif (port == 1): 
        trig = trigr
        echo = echor
    elif (port == 2):
        trig = trigw
        echo = echow
    else:
        trig = trigf
        echo = echof

    GPIO.output(trig, True) 
    time.sleep(0.00001)
    GPIO.output(trig, False)
    start_time = time.time()
    stop_time = time.time()
    while GPIO.input(echo) == 0:
        start_time = time.time()
    while GPIO.input(echo) == 1:
        stop_time = time.time()
    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2
    return distance

def get_inital():
    inital_wall_dis = get_ultra(2)
    inital_front_dis = get_ultra(3)
    inital_diff = abs(inital_wall_dis - inital_front_dis)

def s_forward():
    dw = get_ultra(2)
    df = get_ultra(3)
    if ((dw > df) and ((dw-df) > (inital_diff+1))):
        turn_right(0.15)
        forward()
    elif ((df > dw) and ((df-dw) > (inital_diff+1))):
        turn_left(0.1)
        forward()
    else:
        forward()
    sleep(0.1)

def fix_bias():
    dw = get_ultra(2)
    df = get_ultra(3)
    while (abs(dw-df) > (inital_diff+1)):
        if (dw > df):
            turn_right(0.1)
            sleep(0.2)
        elif (df > dw):
            turn_left(0.1)
            sleep(0.2)
        dw = get_ultra(2)
        df = get_ultra(3)

def guide_slave():
    dl = get_ultra(0)
    dr = get_ultra(1)
    while ((dl < 50) and (dr < 50)):
        s_forward()
        pause()
        dl = get_ultra(0)
        dr = get_ultra(1)
    fix_bias()

    print("dl=",dl)
    print("dr=",dr)
    while ((dl > 20) and (dr > 20)):
        if (abs(dl-dr) > 20):
            print("dl=",dl)
            print("dr=",dr)
            if ((dl > 2000) and (dr > 2000)):   # Two Sides Covered
                bluet(4)
                bluet(0)
                print("2 covered")
            elif ((dr >2000) or (dl > 2000)):
                dl = get_ultra(0)
                dr = get_ultra(1)
                continue
            elif ((dl > 1200 ) and (dr > 1200)):  # Two Sides Miss
                bluet(0)
                print("break")
                break
            elif (dl > dr):     
                bluet(2)
                print("turn left")
            else:
                bluet(3)
                print("turn right")
        else:
            bluet(1)
            bluet(0)
        sleep(0.1)
        dl = get_ultra(0)
        dr = get_ultra(1)
    bluet(0)

# Alexa API
@ask.launch
def launch():
    speech_text = 'Welcome to Raspberry Pi Automation, start now?'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)

@ask.intent('ControlCar')
def Master(device,direction):
    if device in MASTER:
        if direction in PAUSE:
            pause()
            return statement('Okay, master is stopped.')
        elif direction in FORWARD:
            locating()
            get_inital()
            guide_slave()
            pause()
            return statement('Master now run and slave will follow.')
        elif direction in BACKWARD:
            backward()
            sleep(0.5)
            pause()
            return statement('Okay, master go backward.')
        elif direction in RIGHT:
            turn_right(0.5)
            return statement('Okay, master turn right.')
        elif direction in LEFT:
            turn_left(0.4)
            return statement('Okay, master turn left.')
        else:
            return statement('Sorry, that is not supported.')
    elif device in SLAVE:
        if direction in PAUSE:
            bluet(0)
            return statement('Okay, Slave is stopped.')
        elif direction in FORWARD:
            bluet(1)
            return statement('Okay, Slave go forward.')
        elif direction in BACKWARD:
            bluet(4)
            return statement('Okay, slave go backward.')
        elif direction in RIGHT:
            bluet(2)
            return statement('Okay, slave turn right.')
        elif direction in LEFT:
            bluet(3)
            return statement('Okay, slave turn left.')
        else:
            return statement('Sorry, that is not supported.')
    else:
        mes = 'Which car?'
        return question(mes).reprompt(mes).simple_card(mes)

@ask.intent('AMAZON.AMAZON.StopIntent')
def stopI():
    pause()
    return statement('Okay, vehicle is stopped.')

@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)

@ask.intent('AMAZON.CancelIntent')
def cancelI():
    pause()
    return statement('Okay, goodbye.')

@ask.session_ended
def end():
    pause()
    return statement('Okay, system shutdown.')


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)