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


# Main loop
while 1:
    if controller_1.buttonRight.pressing():
        pass
        # autonomous()
    if controller_1.buttonLeft.pressing():
        while 1:
            drivingsimple()
    wait(5, MSEC)

    


