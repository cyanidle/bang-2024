#!/usr/bin/env python
import atexit
from threading import Thread
from time import sleep
from bang import *

def Task(func):
    Thread(target=func, daemon=True).start()
    return func

P = 450
I = 600
D = 1

def make_motor(num, angle):
    return MsgConfigMotor(
        num, 
        radius=0.18,
        maxSpeed=0.55,
        turnMaxSpeed=0.25,
        ticksPerRotation=360,
        propCoeff=P,
        interCoeff=I,
        diffCoeff=D,
        coeff=1,
        angleDegrees=angle
    )

motors = [
    make_motor(0, 90),
    make_motor(1, 210),
    make_motor(2, 330),
]

pinouts = [
    MsgConfigPinout(num = 0, encoderA=18, encoderB=31, enable=12, fwd=34, back=35),
    MsgConfigPinout(num = 1, encoderA=19, encoderB=38, enable=8, fwd=37, back=36),
    MsgConfigPinout(num = 2, encoderA=3, encoderB=49, enable=9, fwd=43, back=42),
]

bang = Bang(lidar_uri = None)
odom = Odom(motors)

POS = Position(0, 0, 0)

@bang.arduino.on(MsgOdom)
def handle_odom(msg):
    odom.handle(msg)
    if odom.hits >= 6:
        POS = odom.update()

@bang.arduino.on(MsgEcho)
def handle_echo(echo): print(f"<== {echo}")
@bang.arduino.on(MsgTest)
def handle_test(msg): print(f"Test: {msg}")

def move(x, y, z): bang.arduino.send(MsgMove(x, y, z))
def stop(): move(0, 0, 0)

def forward(x): move(x, 0, 0)
def right(y): move(0, y, 0)
def turn(z): move(0, 0, z)

for params, pinout in zip(motors, pinouts):
    sleep(0.3)
    bang.arduino.send(pinout)
    sleep(0.3)
    bang.arduino.send(params)

def shutdown():
    global bang
    stop()
    del bang
    sleep(0.3)

atexit.register(shutdown)

START_PIN = 48
START_ROUND = False

@bang.arduino.on(MsgReadPin)
def handle_pin(msg: MsgReadPin): 
    global START_ROUND
    print(f"Got pin: {msg}")
    if msg.value and msg.pin == START_PIN:
        print("Starting round")
        START_ROUND = True


def start():
    sleep(0.5)
    while True: 
        forward(1000)
        sleep(3)
        turn(1000)
        sleep(3)
        turn(-1000)

while True:
    sleep(0.1)
    bang.arduino.send(MsgReadPin(START_PIN, 0, pullup=1))
    if START_ROUND:
        start()
        break