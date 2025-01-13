from flask import Flask
from flask_socketio import SocketIO
import RPi.GPIO as GPIO
import threading
import signal
import sys
import json
import os

from logger.logger import setup_logger
from routes import register_routes

class App:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.logger = setup_logger()
        
        self.app = Flask(__name__, template_folder='../html/templates', static_folder="../pictures")
        self.load_config()
        self.socketio = SocketIO(self.app)

        signal.signal(signal.SIGINT, self.signal_handler)

        self.stop_event = threading.Event()

    def load_config(self):
        with open(self.config_file) as f:
            config = json.load(f)
            self.app.config.update(config)

    def create_app(self):
        register_routes(self.app)
        return self.app
    
    def cleanup(self):
        GPIO.cleanup()
        self.stop_event.set()

    def signal_handler(self, sig, frame):
        self.cleanup()
        sys.exit(0)


if __name__ == '__main__':
    config_file = os.path.join(os.path.dirname(__file__), '../files/config.json')
    config = App(config_file=config_file)
    app_instance = config.create_app()

    try:
        config.socketio.run(app=app_instance, debug=True)
    finally:
        config.cleanup()
