import RPi.GPIO as GPIO
import time

class Stepper:
    """
    A class to represent the stepper motor and its related operations.
    """

    def __init__(self, pins, delay_between_steps, left_button_pin, right_button_pin):
        """
        Initialize the stepper motor.

        Args:
            pins (list): GPIO pins used for the stepper motor.
            delay_between_steps (float): Delay between steps in seconds.
            left_button_pin (int): GPIO pin for the left button.
            right_button_pin (int): GPIO pin for the right button.
        """
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
        """
        Initialize and calibrate the stepper motor.

        Returns:
            str: A message indicating the stepper motor's initialization status.
        """
        self.move_to_left_end()
        self.move_to_right_end()
        self.move_to_left_end()
        return "Stepper motor initialized and calibrated"

    def move_to_left_end(self):
        """
        Move the stepper motor to the left end.
        """
        while GPIO.input(self.left_button_pin) == GPIO.HIGH:
            self.move_left_step()
        self.current_pos = 0

    def move_to_right_end(self):
        """
        Move the stepper motor to the right end.
        """
        while GPIO.input(self.right_button_pin) == GPIO.HIGH:
            self.move_right_step()
        self.current_pos = 100  # Example value, adjust as needed

    def move_left_step(self):
        """
        Move the stepper motor one step to the left.
        """
        # Implement the logic to move the stepper motor one step to the left
        time.sleep(self.delay_between_steps)

    def move_right_step(self):
        """
        Move the stepper motor one step to the right.
        """
        # Implement the logic to move the stepper motor one step to the right
        time.sleep(self.delay_between_steps)

    def move_to_position(self, steps):
        """
        Move the stepper motor to a specified position.

        Args:
            steps (int): The target position in steps.

        Returns:
            str: A message indicating the stepper motor's new position.
        """
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
        """
        Move the stepper motor one step to the right.

        Returns:
            str: A message indicating the stepper motor's new position.
        """
        self.move_right_step()
        self.current_pos += 1
        return f"Moved right to position {self.current_pos}"

    def move_left(self):
        """
        Move the stepper motor one step to the left.

        Returns:
            str: A message indicating the stepper motor's new position.
        """
        self.move_left_step()
        self.current_pos -= 1
        return f"Moved left to position {self.current_pos}"

    def speed_adjuster(self, speed):
        """
        Adjust the speed of the stepper motor.

        Args:
            speed (float): The new delay between steps in seconds.

        Returns:
            str: A message indicating the new speed.
        """
        self.delay_between_steps = speed
        return f"Speed adjusted to {speed}"

    def get_current_pos(self):
        """
        Get the current position of the stepper motor.

        Returns:
            dict: A dictionary containing the current position.
        """
        return {"current_pos": self.current_pos}

    def set_current_pos(self, pos):
        """
        Set the current position of the stepper motor.

        Args:
            pos (int): The new current position.

        Returns:
            str: A message indicating the new current position.
        """
        self.current_pos = pos
        return f"Current position set to {self.current_pos}"
