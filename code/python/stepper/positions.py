import json
import logging

logger = logging.getLogger('my_logger')

class PositionManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.positions = []

    def load_positions(self):
        try:
            with open(self.file_path) as f:
                positions_data = json.load(f)
                self.positions = positions_data['positions']
                logger.debug('Successfully read positions.json')
        except Exception as e:
            logger.error(f'Error reading positions.json: {e}')
            return []

        return self.positions
