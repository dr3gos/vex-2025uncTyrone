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
spinnerMotor = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
intakeMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
trapMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)

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

def trapForward():
    # if controller_1.buttonR1.pressing():
    #     power = 100
    # elif controller_1.buttonL1.pressing():
    #     power = -100
    # else:
    #     power = 0

    trapMotor.set_velocity(100, PERCENT)
    trapMotor.spin(FORWARD)

# def trapBackward():
#     if controller_1.buttonL1.pressing():
#         trapMotor.set_velocity(100, PERCENT)
#         trapMotor.spin(REVERSE)
#     else:
#         trapMotor.stop()
    

def trapStop():
    trapMotor.stop()

def intake(positive, negative):
    if controller_1.buttonR2.pressing():
        power = positive
    elif controller_1.buttonL2.pressing():
        power = negative
    else:
        power = 0
    intakeMotor.set_velocity(power, PERCENT)
    spinnerMotor.set_velocity(power, PERCENT)
    intakeMotor.spin(FORWARD)
    spinnerMotor.spin(FORWARD)

trapToggle = 0

# Main loop
while 1:
    if controller_1.buttonRight.pressing():
        pass
        # autonomous()
    if controller_1.buttonLeft.pressing():
        while 1:
            drivingsimple()
            intake(100, -100)
            # trapBackward()
            # controller_1.screen.clear_screen()
            # controller_1.screen.print(trapToggle)
            if controller_1.buttonR1.pressing():
                if trapToggle == 0:
                    trapForward()
                elif trapToggle == 1:
                    trapStop()
                # break
                trapToggle = 1 - trapToggle
            


    wait(5, MSEC)

    


