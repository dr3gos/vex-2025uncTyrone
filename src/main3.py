# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main2.py                                                     #
# 	Project:      AISB VEX 24'-25' Unc Tyrone                                  #
# 	Author:       Dragos S.                                                    #
# 	Created:      30/01/2025                                                   #
# 	Description:  Massive optimizations                                        #
#                                                                              #
# ---------------------------------------------------------------------------- #


from vex import *

# ---------------------------- Constants & Enums ------------------------------
DEADBAND_THRESHOLD = 5
MOTOR_VELOCITY = 100  # Percentage

class Mode:
    DISABLED = 0
    AUTONOMOUS = 1
    DRIVER = 2

class IntakeState:
    STOPPED = 0
    FORWARD = 1
    REVERSE = 2

# -------------------------- Hardware Initialization ---------------------------
brain = Brain()
controller = Controller()

# Motor configuration with optional brake mode
def configure_motor(port, reverse=False):
    return Motor(port, GearSetting.RATIO_18_1, reverse, BRAKE)

left_motor = configure_motor(Ports.PORT3)
right_motor = configure_motor(Ports.PORT4)
intake = configure_motor(Ports.PORT5)
spinner = configure_motor(Ports.PORT6)
trapper = configure_motor(Ports.PORT7)

# ---------------------------- State Management -------------------------------
class RobotState:
    def __init__(self):
        self.mode = Mode.DISABLED
        self.intake_state = IntakeState.STOPPED
        self.trapper_toggled = False
        self.last_buttons = {'L2': False, 'R2': False, 'A': False}

robot_state = RobotState()

# ---------------------------- Control Functions -------------------------------
def apply_deadband(value):
    return value if abs(value) > DEADBAND_THRESHOLD else 0

def drive_control():
    forward = apply_deadband(-controller.axis3.position())
    turn = apply_deadband(controller.axis1.position())
    
    # Differential drive calculation
    left = forward + turn
    right = forward - turn
    
    # Constrain and apply motor speeds
    left = max(-100, min(left, 100))
    right = max(-100, min(right, 100))
    
    left_motor.spin(FORWARD, left, PERCENT)
    right_motor.spin(FORWARD, right, PERCENT)

def update_intake_spinner():
    L2 = controller.buttonL2.pressing()
    R2 = controller.buttonR2.pressing()
    
    # Toggle logic with edge detection
    if L2 and not robot_state.last_buttons['L2']:
        robot_state.intake_state = (IntakeState.FORWARD 
            if robot_state.intake_state != IntakeState.FORWARD 
            else IntakeState.STOPPED)
    
    if R2 and not robot_state.last_buttons['R2']:
        robot_state.intake_state = (IntakeState.REVERSE 
            if robot_state.intake_state != IntakeState.REVERSE 
            else IntakeState.STOPPED)
    
    # State execution
    if robot_state.intake_state == IntakeState.FORWARD:
        intake.spin(FORWARD, MOTOR_VELOCITY, PERCENT)
        spinner.spin(FORWARD, MOTOR_VELOCITY, PERCENT)
    elif robot_state.intake_state == IntakeState.REVERSE:
        intake.spin(REVERSE, MOTOR_VELOCITY, PERCENT)
        spinner.spin(REVERSE, MOTOR_VELOCITY, PERCENT)
    else:
        intake.stop()
        spinner.stop()
    
    # Update button states
    robot_state.last_buttons['L2'] = L2
    robot_state.last_buttons['R2'] = R2

def update_trapper():
    A = controller.buttonA.pressing()
    B = controller.buttonB.pressing()
    
    # Toggle on rising edge of A
    if A and not robot_state.last_buttons['A']:
        robot_state.trapper_toggled = not robot_state.trapper_toggled
    
    # Priority to manual override (B button)
    if B:
        trapper.spin(REVERSE, MOTOR_VELOCITY, PERCENT)
    elif robot_state.trapper_toggled:
        trapper.spin(FORWARD, MOTOR_VELOCITY, PERCENT)
    else:
        trapper.stop()
    
    robot_state.last_buttons['A'] = A

def stop_all_motors():
    left_motor.stop()
    right_motor.stop()
    intake.stop()
    spinner.stop()
    trapper.stop()

# ---------------------------- Mode Management --------------------------------
def handle_mode_switching():
    # Emergency stop using X button
    if controller.buttonX.pressing():
        robot_state.mode = Mode.DISABLED
        return
    
    if robot_state.mode == Mode.DISABLED:
        if controller.buttonLeft.pressing():
            robot_state.mode = Mode.AUTONOMOUS
        elif controller.buttonRight.pressing():
            robot_state.mode = Mode.DRIVER

def autonomous():
    # !!! Autonomous code goes here !!!
    pass

def driver_control():
    drive_control()
    update_intake_spinner()
    update_trapper()

# ---------------------------- Main Execution ----------------------------------
def main_loop():
    while True:
        handle_mode_switching()
        
        if robot_state.mode == Mode.AUTONOMOUS:
            autonomous()
        elif robot_state.mode == Mode.DRIVER:
            driver_control()
        else:
            stop_all_motors()
        
        wait(20, MSEC)

# Start program execution
main_loop()