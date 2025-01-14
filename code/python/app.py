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
        self.logger = setup_logger()

        self.config_file = config_file
        
        try:
            self.app = Flask(__name__, template_folder='../html/templates', static_folder="../html/static")
            self.logger.debug('initialized Flask app')
        except Exception as e:
            self.logger.error(e)

        try:
            self.load_config()
            self.logger.debug('loaded config')
        except Exception as e:
            self.logger.error(e)
        
        try:
            self.socketio = SocketIO(self.app)
            self.logger.debug('initialized SocketIO')
        except Exception as e:
            self.logger.error('failed to initialized SocketIO {e}')

        try:
            signal.signal(signal.SIGINT, self.signal_handler)
            self.logger.debug('setup signalhandler')
        except Exception as e:
            self.logger.error('failed to setup signalhandler: {e}')
        
        self.stop_event = threading.Event()

    def load_config(self):
        with open(self.config_file) as f:
            config = json.load(f)
            self.app.config.update(config)

    def create_app(self):
        try:
            register_routes(self.app)
            self.logger.debug('registered routes to flask app')
        except Exception as e:
            self.logger.error('failed to register routes to flask app: {e}')
        return self.app
    
    def cleanup(self):
        GPIO.cleanup()
        self.logger.debug('GPIO cleanup complete')
        self.logger.debug('-' * 40)
        self.logger.debug('-' * 40)
        self.logger.debug('-' * 40)
        self.logger.debug('-' * 40)
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
