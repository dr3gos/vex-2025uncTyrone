# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Project:      AISB VEX 23'-24' Test Code                                   #
# 	Author:       Dragos S.                                                    #
# 	Created:      31/10/2024                                                   #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

        
# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

brain.screen.print("Hello V5")

controller_1 = Controller(PRIMARY)
leftRear = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)       
rightRear = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
sucker = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
pneumatic = DigitalOut(brain.three_wire_port.a)

wait(30, MSEC)

# Functions

# Driving function


def drivingsimple():
    speed = -controller_1.axis3.position() #updown left
    # strafe = controller_1.axis4.position() #leftright left
    turn = controller_1.axis1.position()  #leftright right

    leftRearPower = (speed - turn)
    rightRearPower = (speed + turn)

    leftRear.set_velocity(leftRearPower, PERCENT)
    rightRear.set_velocity(rightRearPower, PERCENT)

    leftRear.spin(FORWARD)
    rightRear.spin(FORWARD)

def operate_sucker():
    sucker.set_velocity(100, PERCENT)
    if controller_1.buttonR2.pressing():
        sucker.spin(REVERSE)
        wait(5, MSEC)
    if controller_1.buttonL2.pressing():
        sucker.spin(FORWARD)
        wait(5, MSEC)
    else:
        sucker.stop()

def pneumaticControl():
    if controller_1.buttonA.pressing():
        pneumatic.set(True)
    if controller_1.buttonB.pressing():
        pneumatic.set(False)

# Main loop
while 1:
    if controller_1.buttonRight.pressing():
        pass
        # autonomous()
    if controller_1.buttonLeft.pressing():
        while 1:
            drivingsimple()
            operate_sucker()
            pneumaticControl()
    wait(5, MSEC)

    


