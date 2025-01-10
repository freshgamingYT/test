import RPi.GPIO as GPIO
import time

class Stepper:
    def __init__(self, step_pin, direction_pin, enable_pin, delay_between_steps, left_button_pin, right_button_pin):
        GPIO.setwarnings(False)
        self.step_pin = step_pin
        self.direction_pin = direction_pin
        self.enable_pin = enable_pin
        self.delay_between_steps = delay_between_steps
        self.left_button_pin = left_button_pin
        self.right_button_pin = right_button_pin
        self.current_pos = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.setup(self.left_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.right_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def init(self):
        try:
            self.move_to_left_end()
            self.move_to_right_end()
            self.move_to_left_end()
            return "Stepper motor initialized and calibrated"
        except Exception as e:
            return f"Error initializing stepper motor: {e}"

    def move_to_left_end(self):
        try:
            while GPIO.input(self.left_button_pin) == GPIO.HIGH:
                self.move_left_step()
            self.current_pos = 0
        except Exception as e:
            print(f"Error moving to left end: {e}")

    def move_to_right_end(self):
        try:
            while GPIO.input(self.right_button_pin) == GPIO.HIGH:
                self.move_right_step()
            self.current_pos = 100  # Example value, adjust as needed
        except Exception as e:
            print(f"Error moving to right end: {e}")

    def move_left_step(self):
        GPIO.output(self.direction_pin, GPIO.LOW)
        GPIO.output(self.step_pin, GPIO.HIGH)
        time.sleep(self.delay_between_steps)
        GPIO.output(self.step_pin, GPIO.LOW)
        time.sleep(self.delay_between_steps)

    def move_right_step(self):
        GPIO.output(self.direction_pin, GPIO.HIGH)
        GPIO.output(self.step_pin, GPIO.HIGH)
        time.sleep(self.delay_between_steps)
        GPIO.output(self.step_pin, GPIO.LOW)
        time.sleep(self.delay_between_steps)

    def cleanup(self):
        GPIO.cleanup()

# Example usage
if __name__ == "__main__":
    stepper = Stepper(step_pin=17, direction_pin=27, enable_pin=22, delay_between_steps=0.01, left_button_pin=5, right_button_pin=6)
    try:
        stepper.init()
    finally:
        stepper.cleanup()
