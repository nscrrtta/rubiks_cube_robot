import time


# Number of motor steps in one 90 degree turn
NUM_STEPS = 400

# Delay between motor steps (microseconds)
STEP_DELAY = 50

# Converts seconds to microseconds
MICRO_SLEEP = lambda x: time.sleep(x/1_000_000)

# Enable pin (common to all motor drivers)
ENABLE_PIN = 21

F_MOTOR_STEP_PIN = 6
F_MOTOR_DIR_PIN  = 5

B_MOTOR_STEP_PIN = 22
B_MOTOR_DIR_PIN  = 23

L_MOTOR_STEP_PIN = 25
L_MOTOR_DIR_PIN  = 24

R_MOTOR_STEP_PIN = 27
R_MOTOR_DIR_PIN  = 17

D_MOTOR_STEP_PIN = 16
D_MOTOR_DIR_PIN  = 26
