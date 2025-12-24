from .constants import *
# import RPi.GPIO as GPIO


class Motors:

    def __init__(self):
        self.pin_dict = {
            'F': (F_MOTOR_STEP_PIN, F_MOTOR_DIR_PIN),
            'B': (B_MOTOR_STEP_PIN, B_MOTOR_DIR_PIN),
            'L': (L_MOTOR_STEP_PIN, L_MOTOR_DIR_PIN),
            'R': (R_MOTOR_STEP_PIN, R_MOTOR_DIR_PIN),
            'D': (D_MOTOR_STEP_PIN, D_MOTOR_DIR_PIN)
        }

        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(ENABLE_PIN, GPIO.OUT)
        # for step_pin, dir_pin in self.pin_dict.values():
            # GPIO.setup(step_pin, GPIO.OUT)
            # GPIO.setup(dir_pin, GPIO.OUT)

        self.set_enable_pin(1)


    def set_enable_pin(self, state: int):
        """
        If enable pin is low, motors can turn
        If enable pin is high, motors can't turn
        """
        # GPIO.output(ENABLE_PIN, state)
        self.busy = not state


    def turn(self, move1: str, move2: str):
        step_pin_i, steps_i = self._set_direction_pin(move1)
        step_pin_j, steps_j = self._set_direction_pin(move2)

        while steps_i or steps_j:
            # if steps_i: GPIO.output(step_pin_i, 1)
            # if steps_j: GPIO.output(step_pin_j, 1)
            MICRO_SLEEP(STEP_DELAY)
            if steps_i: steps_i -= 1 #; GPIO.output(step_pin_i, 0)
            if steps_j: steps_j -= 1 #; GPIO.output(step_pin_j, 0)
            MICRO_SLEEP(STEP_DELAY)

    
    def _set_direction_pin(self, move: str) -> tuple[int]:
        if move is None: return 0, 0

        face, turns = move[0], move[1]
        step_pin, dir_pin = self.pin_dict[face]

        if   turns == '1': steps = 400 #; GPIO.output(dir_pin, 0)
        elif turns == '2': steps = 800 # Direction doesn't matter
        elif turns == '3': steps = 400 #; GPIO.output(dir_pin, 1)

        return step_pin, steps


    def cleanup_pins(self):
        # GPIO.cleanup()
        pass
