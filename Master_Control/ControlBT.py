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
p2.start(21)     # Left

pwml = 15
pwmr = 16

inital_wall_dis = 20
inital_front_dis = 20
inital_diff = 0

print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("enter-info g-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")

def right_callback(channel):  # callback function
    global pulser, elapser, start_timer_right
    pulser += 1                                 # increase pulse by 1 whenever interrupt occurred
    elapser = time.time() - start_timer_right   # elapse for every 1 complete rotation made!
    start_timer_right = time.time()             # let current time equals to start_timer


def left_callback(channel):
    global pulsel, elapsel, start_timer_left
    pulsel += 1
    elapsel = time.time() - start_timer_left
    start_timer_left = time.time()


def get_speed(left):
    global rpml, rpmr
    if (left == True):
        if elapsel != 0:
            rpml = 1 / elapsel
            return rpml
    else:
        if elapser != 0:
            rpmr = 1 / elapser
            return rpmr
    return None

def init_interrupt():
    GPIO.add_event_detect(speedl,
                          GPIO.FALLING,
                          callback=left_callback,
                          bouncetime=20)
    GPIO.add_event_detect(speedr,
                          GPIO.FALLING,
                          callback=right_callback,
                          bouncetime=20)

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

def changePWM(left,offset):
    if (left):
        p2.ChangeDutyCycle(pwml + offset)
    else:
        p1.ChangeDutyCycle(pwmr + offset)

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

def get_inital():
    inital_wall_dis = get_ultra(2)
    inital_front_dis = get_ultra(3)
    inital_diff = abs(inital_wall_dis - inital_front_dis)
    print("ini w=", inital_wall_dis)
    print("ini f=", inital_front_dis)
    print("ini d=", inital_diff)

def s_forward():
    dw = get_ultra(2)
    df = get_ultra(3)
    if ((dw > df) and ((dw-df) > (inital_diff+1))):
        turn_right(0.1)
        forward()
        sleep(0.1)
    elif ((df > dw) and ((df-dw) > (inital_diff+1))):
        turn_left(0.1)
        forward()
        sleep(0.1)
    else:
        forward()
        sleep(0.3)

def fix_bias():
    dw = get_ultra(2)
    df = get_ultra(3)
    while (abs(dw-df) > (inital_diff+3)):
        if (dw > df):
            turn_right(0.1)
            sleep(0.2)
        elif (df > dw):
            turn_left(0.1)
            sleep(0.2)
        dw = get_ultra(2)
        df = get_ultra(3)
     
def destory():
    GPIO.cleanup()
    # bus.close()

if __name__ == '__main__':
    init_interrupt()

    try:
        while (1):
            x = input()

            if (x == 'g'):
                print("test")
                get_inital()
                while (1):
                    dl = get_ultra(0)
                    dr = get_ultra(1)
                    print("dl=",dl,"dr=",dr)
                    if (abs(dl-dr) > 15):
                        bluet(0)           
                        pause()
                        fix_bias()
                        if ((dl > 1500) and (dr > 1500)):   # Two Sides Covered
                            bluet(4)
                            bluet(0)
                            print("2 covered")
                        elif ((dl > 150 ) and (dr > 150)):  # Two Sides Miss
                            bluet(0)
                            print("break")
                            break
                        elif ((dl > 100) or (dr > 1500)):   # Right Side Too Close/Covered
                            bluet(4)    
                            bluet(0)
                            bluet(2)
                            print("righr covered")
                        elif ((dr > 100) or (dl > 1500)):   # Left Side Too Close/Covered
                            bluet(4)    
                            bluet(0)
                            bluet(3)
                            print("left covered")
                        elif (dl > dr):     
                            bluet(2)
                            print("turn left")
                        else:
                            bluet(3)
                            print("turn right")
                    elif ((dl < 20) and (dr < 20)): # Too Close -> Speed up
                        bluet(0)
                        s_forward()
                        print("master go")
                    else:                           # Too Far -> Wait
                        pause()
                        fix_bias()
                        bluet(1)
                        bluet(0)
                    sleep(0.15)
                x = 'z'

            elif (x == 's'):
                print("stop")
                bluet(0)
                pause()
                x = 'z'

            elif (x == 'f'):
                print("forward")
                forward()
                x = 'z'

            elif (x == 'b'):
                print("backward")
                backward()
                x = 'z'

            elif (x == 'r'):
                print("Turn Right")
                turn_right(0.1)
                x = 'z'

            elif (x == 'l'):
                print("Turn Left")
                turn_left(0.1)
                x = 'z'

            elif (x == 'e'):
                destory()
                break

            else:
                # Playground Start
                sl = get_speed(False)
                sr = get_speed(True)
                dl = get_ultra(0)
                dr = get_ultra(1)
                dw = get_ultra(2)
                df = get_ultra(3)
                print("Dis Left: ", dl)
                print("Dis Right: ", dr)
                print("Dis Wall: ", dw)
                print("Dis Front: ", df)
                print("Wheel Speed Left: ", sl)
                print("Wheel Speed Right: ", sr)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, release GPIO
        destory()
