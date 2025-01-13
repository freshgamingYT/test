import json
import math
import logging

logger = logging.getLogger('my_logger')

class PositionManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.positions_2d_array = []

    def load_positions(self):
        try:
            with open(self.file_path) as f:
                positions_dict = json.load(f)
                logger.debug('Successfully read positions.json')
        except Exception as e:
            logger.error(f'Error reading positions.json: {e}')
            return

        positions_list = list(positions_dict.values())
        num_rows = 2  # You can change this to any number of rows you want
        num_columns = math.ceil(len(positions_list) / num_rows)
        self.positions_2d_array = [positions_list[i:i + num_columns] for i in range(0, len(positions_list), num_columns)]
        logger.debug(f'2D array: {self.positions_2d_array}')
