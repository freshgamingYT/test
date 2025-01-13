import json
import logging

logger = logging.getLogger('my_logger')

class ButtonManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.buttons = []

    def load_buttons(self):
        try:
            with open(self.file_path) as f:
                data = json.load(f)
                self.buttons = data['buttons']
                logger.debug('Successfully read buttons.json')
        except Exception as e:
            logger.error(f'Error reading buttons.json: {e}')
