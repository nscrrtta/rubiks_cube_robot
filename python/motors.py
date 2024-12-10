from constants import *
import RPi.GPIO as GPIO


class Motors:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ENABLE_PIN, GPIO.OUT)
        
        self.driver_dict = {
            'F': Driver(F_MOTOR_STEP_PIN, F_MOTOR_DIR_PIN),
            'B': Driver(B_MOTOR_STEP_PIN, B_MOTOR_DIR_PIN),
            'L': Driver(L_MOTOR_STEP_PIN, L_MOTOR_DIR_PIN),
            'R': Driver(R_MOTOR_STEP_PIN, R_MOTOR_DIR_PIN),
            'D': Driver(D_MOTOR_STEP_PIN, D_MOTOR_DIR_PIN)
        }

        self.set_enable_pin(1)


    def set_enable_pin(self, state:int):
        """
        If enable pin is low, motors can turn
        If enable pin is high, motors can't turn
        """
        GPIO.output(ENABLE_PIN, state)
        self.busy = not state


    def turn(self, move1:str, move2:str):
        """
        move: 2-character string
        example: 'F1'

        1st character {'F', 'B', 'L', 'R', 'D'}:
            'F' -> Front-face motor
            'B' -> Back-face motor
            'L' -> Left-face motor
            'R' -> Right-face motor
            'D' -> Down-face motor

        2nd character {'1', '2', '3'}: 
            '1' -> 90 degree turn clockwise
            '2' -> 180 degree turn (direction doesn't matter)
            '3' -> 90 degree turn counter-clockwise
        """

        driver1 = self.driver_dict[ move1[0] ]
        if   move1[1] == '1': i = 400; GPIO.output(driver1.dir_pin, 0)
        elif move1[1] == '2': i = 800  # Direction doesn't matter
        elif move1[1] == '3': i = 400; GPIO.output(driver1.dir_pin, 1)

        if move2 is not None:
            driver2 = self.driver_dict[ move2[0] ]
            if   move2[1] == '1': j = 400; GPIO.output(driver2.dir_pin, 0)
            elif move2[1] == '2': j = 800  # Direction doesn't matter
            elif move2[1] == '3': j = 400; GPIO.output(driver2.dir_pin, 1)
        else: j = 0

        # i = number of steps remaining for move 1
        # j = number of steps remaining for move 2
        while i or j:
            if i: GPIO.output(driver1.step_pin, 1)
            if j: GPIO.output(driver2.step_pin, 1)
            MICRO_SLEEP(STEP_DELAY)
            if i: i -= 1; GPIO.output(driver1.step_pin, 0)
            if j: j -= 1; GPIO.output(driver2.step_pin, 0)
            MICRO_SLEEP(STEP_DELAY)


    def cleaup_pins(self):
        GPIO.cleanup()


class Driver:

    def __init__(self, step_pin:int, dir_pin:int):
        self.step_pin = step_pin
        self.dir_pin  = dir_pin

        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin,  GPIO.OUT)
