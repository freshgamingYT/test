from flask import Blueprint, render_template, request, jsonify, send_from_directory
from stepper.movement import Movement  # Import the Movement class
import logging
import os

logger = logging.getLogger('my_logger')

cocktail_route = Blueprint('cocktail_route', __name__)
main_route = Blueprint('main_route', __name__)

movement = Movement(
    positions_file='../files/positions.json',
    sequence_file='../files/sequence.json',
    config_file='../files/config.json'
)  # Initialize the Movement class

@cocktail_route.route('/1', methods=['GET'])
def cocktail():
    logger.debug('Serving C1.html')
    return render_template('C1.html')

@cocktail_route.route('/start', methods=['POST'])
def start():
    data = request.get_json()
    logger.debug(f'Received start button press: {data}')
    if data['button'] == 'start':
        # Execute the sequence of movements
        movement.execute_sequence()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'failed'})

@main_route.route('/', methods=['GET'])
def index():
    logger.debug('Serving index.html')
    return render_template('index.html')

@main_route.route('/pictures/<path:filename>')
def pictures(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), '../pictures'), filename)

def register_routes(app):
    app.register_blueprint(cocktail_route, url_prefix="/cocktail")
    app.register_blueprint(main_route)
    logger.debug('Routes registered successfully')
