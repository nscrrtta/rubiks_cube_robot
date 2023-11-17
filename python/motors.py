import RPi.GPIO as GPIO
import time
usleep = lambda x: time.sleep(x/1_000_000)


""" https://www.raspberrypi.com/documentation/computers/raspberry-pi.html """


step_delay = 50 # Delay between steps (microseconds)
enable_pin = 21 # Enable pin (common to all drivers)


GPIO.setmode(GPIO.BCM)
GPIO.setup (enable_pin, GPIO.OUT)
GPIO.output(enable_pin, 1)


class Motor:

    def __init__(self, step_pin, dir_pin):

        self.step_pin = step_pin
        self.dir_pin  = dir_pin

        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin,  GPIO.OUT)

    def turn(self, n: int):

        num_steps = 800 if n == 2 else 400 # 400 steps in a 90 degree turn

        if   n == 1: GPIO.output(self.dir_pin, 0) # 90 degrees clockwise
        elif n == 3: GPIO.output(self.dir_pin, 1) # 90 degrees counter-clockwise
        
        for _ in range(num_steps):
            GPIO.output(self.step_pin, 1)
            usleep(step_delay)
            GPIO.output(self.step_pin, 0)
            usleep(step_delay)


motor_dict = {
    'F': Motor( 6, 5), # Front motor
    'B': Motor(22,23), # Back  motor
    'L': Motor(25,24), # Left  motor
    'R': Motor(27,17), # Right motor
    'D': Motor(16,26)  # Down  motor
}
