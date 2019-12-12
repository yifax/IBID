# Project IBID
## Interaction Between Intelligent Devices

### Team Members
* Zeyu Wang
* Yifan Xu

### Project Summary
##### Goal
To build a algorithm for autopilot vehicles, which can provide a reliable communication protocol between two or more vehicles.
##### Deliverable
Instead of adding onboard sensors, we want to make the following car to be blind but auto-pilotable basing on the information shared from the leading car. 

### Hardware Used in This Porject
* Arduino Uno
* Raspberry Pi 3B+
* Ultrasonic Sensor
* IR Dectector
* L298N Motor Drive Controller
* HC-05 Bluetooth Chip
* ESP8266 WiFi Chip
* Feasycom Long Range Bluetooth iBeacons
* Echo Dot V3

### Part 1: Interaction between Two Cars: Car Following Algorithm
#### Features
* Leading car have multiple sensors, following car have no sensor.
* Leading car transmits detected environment information to the following car.
* Leading car controls the following car by command signals via Bluetooth channel.
#### Demo
[![Demo Video](/Src/Demo1.png)](https://www.youtube.com/watch?v=8CCx7NysUWU)

### Part 2: Interactions between Cars and Bluetooth Stations: Indoor Positioning System via RSSI
#### Algorithm
* Step 1: Scan the RSSI values
* Step 2: Find out three Bluetooth iBeacons by filtering Bluetooth addresses
* Step 3: Calculate distances between the car and all three iBeacons
* Step 4: Calculate car coordinate pair by applying Heron's formula
* Step 5: Use this coordinate for indoor navigation
#### Demo
[![Demo Video](/Src/Demo2.png)](https://www.youtube.com/watch?v=NX05F57GPa4)

### Part 3: Interactions between Human and Cars: Voice Control Sysyem
#### Features
* Voice commands activate Echo Dot
* Alexa API send Raspberry Pi server processed NLP package: [{Device name}, {Operation name}]
* Raspberry Pi controls Master car directly and controls Slave cars by Bluetooth command signals
#### Demo

