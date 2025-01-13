from stepper.positions import PositionManager  # Import PositionManager
import RPi.GPIO as GPIO
import time
import json
import logging

logger = logging.getLogger('my_logger')

class Movement:
    def __init__(self, positions_file, sequence_file, config_file):
        self.position_manager = PositionManager(file_path=positions_file)
        self.positions = self.position_manager.load_positions()
        self.sequence_file = sequence_file
        self.config = self.load_config(config_file)
        self.step_pin = self.config['GPIO_PINS']['step_pin']
        self.direction_pin = self.config['GPIO_PINS']['direction_pin']
        self.enable_pin = self.config['GPIO_PINS']['enable_pin']
        self.us_delay = self.config['GPIO_PINS']['us_delay']
        self.velocity_slow = self.config['GPIO_PINS']['velocity_slow']
        self.velocity_medium = self.config['GPIO_PINS']['velocity_medium']
        self.velocity_fast = self.config['GPIO_PINS']['velocity_fast']
        self.setup_gpio()
        logger.debug('Successfully loaded config.json')


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
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        logger.debug('GPIO setup complete')

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

    def execute_sequence(self):
        sequence = self.load_sequence()
        for description, wait_time in sequence.items():
            self.move_to_position(description)
            logger.debug(f'Waiting for {wait_time} seconds before moving to the next position')
            time.sleep(wait_time)

# Example usage
if __name__ == "__main__":
    movement = Movement(
        positions_file='../files/positions.json',
        sequence_file='../files/sequence.json',
        config_file='../files/config.json'
    )
    movement.execute_sequence()  # Execute the sequence of movements
