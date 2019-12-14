# Project IBID: Interaction Between Intelligent Devices

## Team Members
* Zeyu Wang
* Yifan Xu

## Project Repositories
[Github](https://github.com/yifax/IBID "Check All Codes")

------------------------------

## Project Introduction
#### Motivation
The original ideas of this project come from one simple question: What if all vehicles on the road are autopiloted? Obviously, drivers like me will be free from manual operations, which is not only boring but also very risky. But, what else? In recent years, we have witnessed a great improvement in Autonomous Vehicles' algorithm, which makes these questions very realistic. Although companies like Tesla and Amazon have already operating Autonomous Vehicles business somehow, those autopiloting cars on the road are working alone. In another word, they assume all other vehicles are human-operated. Therefore, if more than one autonomous vehicles are nearby, should they communicate with each other to bring a better understanding of the environment? Will this kind of extra information help the built-in algorithm to work better? Can this kind of information sharing benefit traffic in the future? We decide to do some research.
#### Goal
To build a algorithm for autopilot vehicles, which can provide a reliable communication protocol between two or more vehicles.
#### Deliverable
Instead of adding onboard sensors, we want to make the following car to be blind but auto-pilotable basing on the information shared from the leading car. 

## Hardware Used in This Porject
* Arduino Uno
* Raspberry Pi 3B+
* HCSR04 Ultrasonic Sensor
* IR Dectector
* L298N Motor Drive Controller
* HC-05 Bluetooth Chip
* ESP8266 WiFi Chip
* Feasycom Long Range Bluetooth iBeacons
* Echo Dot V3

## Part 1: Interaction between Two Cars: Car Following Algorithm
### Design & Features
* Leading car have multiple sensors, following car have no sensor.
* Leading car transmits detected environment information to the following car.
* Leading car controls the following car by command signals via Bluetooth channel.

### Demo
[![Demo Video](/Src/Demo1.png)](https://www.youtube.com/watch?v=8CCx7NysUWU)

### Test Code and Instructions
#### Raspberry Pi GPIO Connection
![GPIO](/Src/GPIO.png)

#### Bluetooth Communication
Default mode of Raspberry Pi onboard bluetooth module is SLAVE ACCEPT, need to change it to MASTER before connect HC-05 on Arduino
```bash
sudo hciconfig hci0 lm master
```
After this, use `Bluetoothctl` tool to scan, pair and trust target HC-05 module.
Then, connect it as software serial port so that we can send commands via Bluetooth channel.
```bash
sudo rfcomm connect hci0 XX:XX:XX:XX:XX:XX
```

#### Run Control Code on Raspberry Pi
```bash
cd IBID/Master_Control
python3 ControlBT.py
```
#### Download Arduino Code to the Following Car
`Slave.ino` in `IBID/Slave_Control/Slave`



## Part 2: Interactions between Cars and Bluetooth Stations: Indoor Positioning System via RSSI
### Process & Algorithm
* Step 1: Use Bluetooth chip to scan the RSSI values
* Step 2: Find out three Bluetooth iBeacons(stations) thru a a Bluetooth addresses filter
* Step 3: Calculate distances between the car and target iBeacons
* Step 4: Calculate car coordinate pair by applying **Heron's formula**
* Step 5: Use this coordinate for indoor navigation

### Demo
[![Demo Video](/Src/Demo2.png)](https://www.youtube.com/watch?v=4V5qMFQUmjc)

### Indoor Positioning Coordinates
![RSSI](/Src/RSSI.jpg)

### Test Code and Instructions
`pybluez` library is necessary for running RSSI code.
```bash
pip install pybluez
cd IBID/Rssi
python3 testblescan.py
```

## Part 3: Interactions between Human and Cars: Voice Control System
### Design & Process
* Make Raspberry Pi to be a `Linux Server`
* Use `Echo Dot`/`Amazon Alexa App` to fetch voice commands
* Build an `Alexa Skill` to do Nature Language Processing in the Cloud
* Utilize `Alexa API` to send Raspberry Pi processed voice commands package, including to main part [{Device name}, {Operation name}]
* Raspberry Pi then follows command to control the leading car directly, and controls the following cars by Bluetooth command signals
* ![voice](/Src/alexa.png)

### Platform and Tools
![voice](/Src/voice.png)

### Demo
[![Demo Video](/Src/Demo3.png)](https://www.youtube.com/watch?v=NX05F57GPa4)


## Final Stage: Combine 3 Parts Together
At last, we combine all three parts above together to make our final demo. In this demo, we use voice to activate the leading car(Master). When leading car moves, it trigers the following algorithm, which guide the following car(Slave) to follow behind but keep a safe distance basing on the information acquired by both the RSSI system and the sensor system.

### Demo
[![Demo Video](/Src/Demo4.png)](https://www.youtube.com/watch?v=pV74apRyUJk)

## Summary
In all, we successfully built a vehicle interaction system(simulation) this quarter including an indoor positioning system, sensor information sharing platform and voice control system. Human players are able to control all registered vehicles in this system simply by voice. Vehicles inside the system, human-operated or not, are able to communicate with each other to achieve simple collaboration like following or obstacle avoiding.
### Strength
* Multiple Interactions: HCI & CCI
* Accuracy: Combine indoor positioning & sensor information sharing
* Performance: NLP on the Cloud and control operation on the Edge
* Unification: Same protocol on multiple cars, both Arduino & Raspberry Pi
### Weakness
* Voice control does not respond 100% correctly
* Need better algorithms & sensors to handle complex situations
* RSSI values sometime fluctuate, especially when the car is too close to a iBeacon 

## Conclusion
Although we don't have enough funding/support to make a test on real vehicles, we believed that our trial is still meaningful and prospective. The Arduino-Raspberry Pi intelligent car system can be regarded as a simulation of what might happen in the future. Currently, we mainly rely on cheap ultrasonic and IR sensors, but the same idea can be realized on Tesla sedan, which should be equipped with much more precise radars for similar purposes. Now we use Bluetooth iBeacons to build an indoor positioning system. When it goes to the outdoor, we can simply change the source to be GPS satellites while keeping the original positioning algorithm structures. What we did was not playing with toy cars, but a low-cost prototype model for the future way of transportation system.
