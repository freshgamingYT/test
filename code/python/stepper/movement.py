from stepper.positions import PositionManager  # Import PositionManager
import RPi.GPIO as GPIO
import time
import json
import logging

logger = logging.getLogger('my_logger')

class Movement:
    def __init__(self, positions_file, sequence_file, config_file):
        try:
            self.position_manager = PositionManager(file_path=positions_file)
            self.positions = self.position_manager.load_positions()
            self.sequence_file = sequence_file
            self.config = self.load_config(config_file)
            self.step_pin = self.config['GPIO_PINS']['step_pin']
            self.direction_pin = self.config['GPIO_PINS']['direction_pin']
            self.enable_pin = self.config['GPIO_PINS']['enable_pin']
            self.left_button_pin = self.config['GPIO_PINS']['left_button_pin']
            self.right_button_pin = self.config['GPIO_PINS']['right_button_pin']
            self.us_delay = self.config['us_delay']
            self.velocity_slow = self.config['velocity_slow']
            self.velocity_medium = self.config['velocity_medium']
            self.velocity_fast = self.config['velocity_fast']
            self.setup_gpio()
            logger.debug('Successfully loaded config.json')
        except Exception as e:
            logger.error(e)


    def load_positions(self, positions_file):
        try:
            with open(positions_file) as f:
                positions_data = json.load(f)
                logger.debug('Successfully read positions.json')
                return positions_data['positions']
        except Exception as e:
            logger.error(f'Error reading positions file: {e}')
            return []

    def load_sequence(self):
        try:
            with open(self.sequence_file) as f:
                sequence_data = json.load(f)
                logger.debug('Successfully read sequence.json')
                return sequence_data['sequence']
        except Exception as e:
            logger.error(f'Error reading sequence file: {e}')
            return {}

    def load_config(self, config_file):
        try:
            with open(config_file) as f:
                config_data = json.load(f)
                logger.debug('Successfully read config.json')
                return config_data
        except Exception as e:
            logger.error(f'Error reading config file: {e}')
            return {}

    def setup_gpio(self):
        try:
        # Set GPIO mode
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(self.step_pin, GPIO.OUT)
            GPIO.setup(self.direction_pin, GPIO.OUT)
            GPIO.setup(self.enable_pin, GPIO.OUT)
            GPIO.setup(self.left_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.right_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.output(self.enable_pin, GPIO.LOW)
            logger.debug('GPIO setup complete')
        except Exception as e:
            logger.error(e)

    def move_to_left_button(self, description) -> None:
        try:
            GPIO.output(self.direction_pin, 0)
            while GPIO.input(self.left_button_pin) == 0:
                delay = self.velocity_medium * self.us_delay
                GPIO.output(self.step_pin, GPIO.HIGH)
                time.sleep(delay)
                GPIO.output(self.step_pin, GPIO.LOW)
            logger.debug('stepper motor initialized')
        except Exception as e:
            logger.error("move_to_left_button hat einen Fehler")
            logger.error(e)
    """
    def move_to_position(self, description):
        position = next((pos for pos in self.positions if pos['description'] == description), None)
        if position:
            target_position = position['value']
            logger.debug(f'Moving to {description}: {target_position}')
            # Example GPIO logic (replace with your actual logic)
            GPIO.output(self.enable_pin, GPIO.HIGH)
            GPIO.output(self.direction_pin, GPIO.HIGH)
            time.sleep(target_position)
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(self.velocity_slow)
            GPIO.output(self.step_pin, GPIO.LOW)
            GPIO.cleanup()
        else:
            logger.error(f'Invalid position description: {description}')
    """

    def execute_sequence(self):
        try:
            logger.debug('loading sequence for cocktail')
            sequence = self.load_sequence()
        except Exception as e:
            logger.error(e)

        try:
            for description, wait_time in sequence.items():
                logger.debug(description)
                self.move_to_left_button()
                logger.debug(f'Waiting for {wait_time} seconds before moving to the next position')
                time.sleep(wait_time)
        except Exception as e:
            logger.error(e)

# Example usage
if __name__ == "__main__":
    movement = Movement(
        positions_file='../files/positions.json',
        sequence_file='../files/sequence.json',
        config_file='../files/config.json'
    )
    movement.execute_sequence()  # Execute the sequence of movements
