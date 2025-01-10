import RPi.GPIO as GPIO
import time

class Stepper:
    def __init__(self, pins, delay_between_steps, left_button_pin, right_button_pin):
        self.pins = pins
        self.delay_between_steps = delay_between_steps
        self.left_button_pin = left_button_pin
        self.right_button_pin = right_button_pin
        self.current_pos = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pins, GPIO.OUT)
        GPIO.setup(self.left_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.right_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def init(self):
        self.move_to_left_end()
        self.move_to_right_end()
        self.move_to_left_end()
        return "Stepper motor initialized and calibrated"

    def move_to_left_end(self):
        while GPIO.input(self.left_button_pin) == GPIO.HIGH:
            self.move_left_step()
        self.current_pos = 0

    def move_to_right_end(self):
        while GPIO.input(self.right_button_pin) == GPIO.HIGH:
            self.move_right_step()
        self.current_pos = 100  # Example value, adjust as needed

    def move_left_step(self):
        # Implement the logic to move the stepper motor one step to the left
        time.sleep(self.delay_between_steps)

    def move_right_step(self):
        # Implement the logic to move the stepper motor one step to the right
        time.sleep(self.delay_between_steps)

    def move_to_position(self, steps):
        if steps > self.current_pos:
            while self.current_pos < steps:
                self.move_right_step()
                self.current_pos += 1
        elif steps < self.current_pos:
            while self.current_pos > steps:
                self.move_left_step()
                self.current_pos -= 1
        return f"Moved to position {steps}"

    def move_right(self):
        self.move_right_step()
        self.current_pos += 1
        return f"Moved right to position {self.current_pos}"

    def move_left(self):
        self.move_left_step()
        self.current_pos -= 1
        return f"Moved left to position {self.current_pos}"

    def speed_adjuster(self, speed):
        self.delay_between_steps = speed
        return f"Speed adjusted to {speed}"

    def get_current_pos(self):
        return {"current_pos": self.current_pos}

    def set_current_pos(self, pos):
        self.current_pos = pos
        return f"Current position set to {self.current_pos}"
