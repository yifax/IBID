import logging
import os

from flask import Flask
from flask_ask import Ask, request, session, question, statement
import RPi.GPIO as GPIO
import time, math
from time import sleep
import serial
import sys

'''
port = serial.Serial("/dev/rfcomm0", baudrate=9600) # necessary env sitting for BT communication
address = 0x48	# default address of PCF8591(A/D)
channel = 0x40  # address for A0 on PCF8591
'''

in1 = 22
in2 = 23
in3 = 24
in4 = 25

ena = 20
enb = 21

temp1 = 1

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(ena, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)

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

def bluet(message):
    print("Bluetooth Command: ", message)
    '''
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
    '''

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
            forward()
            sleep(1)
            pause()
            return statement('Master go forward.')
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
            sleep(0.5)
            pause()
            return statement('Okay, Slave go forward.')
        elif direction in BACKWARD:
            bluet(4)
            sleep(0.5)
            pause()
            return statement('Okay, slave go backward.')
        elif direction in RIGHT:
            bluet(2)
            return statement('Okay, master turn right.')
        elif direction in LEFT:
            bluet(3)
            return statement('Okay, master turn left.')
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
def stopI():
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