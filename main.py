from bang import Bang, MsgOdom, Odom
from bang.gen import MsgConfigMotor, MsgConfigPinout

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

@bang.arduino.on(MsgOdom)
def handle_odom(msg): 
    odom.handle(msg)

for pinout, params in zip(pinouts, motors):
    bang.arduino.send(pinout)
    bang.arduino.send(params)

