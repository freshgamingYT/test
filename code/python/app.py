from flask import Flask
from flask_socketio import SocketIO
import RPi.GPIO as GPIO 

from python.logger.logger import setup_logger

import threading
import signal
import sys

class app:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.logger = setup_logger()
        
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = "Keins123!"
        self.socketio = SocketIO(self.app)

        signal.signal(signal.SIGINT, self.signal_handler)

        self.stop_event = threading.Event()

    def create_app(self):
        return self.app
    
    def cleanup(self):
        GPIO.cleanup()
        self.stop_event.set()

    def signal_handler(self, sig, frame):
        self.cleanup()
        sys.exit(0)


if __name__ == '__main__':
    config_file = ".../files/config"
    config = app(config_file=config_file)
    test = config.create_app()

    try:
        config.socketio.run(app=app, debug=True)
    finally:
        config.cleanup()
