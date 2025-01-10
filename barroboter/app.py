import argparse
import csv
import json
import logging
import sqlite3
from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from stepper import Stepper
from servo import Servo
from scale import Scale
from cocktail import Cocktail

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['IMAGE_FOLDER'] = 'images'

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log', filemode='a')
logger = logging.getLogger()

# Load configuration from JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Control the components of the bar robot.')
parser.add_argument('--disable-servo', action='store_true', help='Disable the servo motor')
parser.add_argument('--disable-scale', action='store_true', help='Disable the scale')
args = parser.parse_args()

# Initialize components
stepper = Stepper(
    pins=config['stepper']['pins'],
    delay_between_steps=config['stepper']['delay_between_steps'],
    left_button_pin=config['stepper']['left_button_pin'],
    right_button_pin=config['stepper']['right_button_pin']
)
servo = Servo()
scale = Scale()
cocktail = Cocktail()

# Set initial states based on command-line arguments
if args.disable_servo:
    servo.disable()

if args.disable_scale:
    scale.disable()

# Servo routes
@app.route('/servo/init', methods=['GET'])
def init_servo():
    logger.info('Initializing servo motor')
    return servo.init()

@app.route('/servo/enable', methods=['POST'])
def enable_servo():
    logger.info('Enabling servo motor')
    return servo.enable()

@app.route('/servo/disable', methods=['POST'])
def disable_servo():
    logger.info('Disabling servo motor')
    return servo.disable()

# Scale routes
@app.route('/scale/init', methods=['GET'])
def init_scale():
    logger.info('Initializing scale')
    return scale.init()

@app.route('/scale/calibrate_scale', methods=['POST'])
def calibrate_scale():
    logger.info('Calibrating scale')
    return scale.calibrate()

@app.route('/scale/enable', methods=['POST'])
def enable_scale():
    logger.info('Enabling scale')
    return scale.enable()

@app.route('/scale/disable', methods=['POST'])
def disable_scale():
    logger.info('Disabling scale')
    return scale.disable()

# Cocktail routes
@app.route('/Cocktail/select_cocktail', methods=['POST'])
def select_cocktail():
    cocktail_name = request.json.get('cocktail')
    cocktail_data = cocktail.select(cocktail_name)
    if isinstance(cocktail_data, dict):
        logger.info(f'Selected cocktail {cocktail_name}')
        return redirect(url_for('show_cocktail', cocktail_name=cocktail_name))
    else:
        logger.warning(f'Cocktail {cocktail_name} not found')
        return cocktail_data

@app.route('/Cocktail/show/<cocktail_name>', methods=['GET'])
def show_cocktail(cocktail_name):
    cocktail_data = cocktail.select(cocktail_name)
    if isinstance(cocktail_data, dict):
        logger.info(f'Showing details for cocktail {cocktail_name}')
        return render_template('cocktail.html', cocktail=cocktail_data)
    else:
        logger.warning(f'Cocktail {cocktail_name} not found')
        return "Cocktail not found", 404

@app.route('/Cocktail/start_mixing', methods=['POST'])
def start_mixing():
    logger.info('Starting mixing process')
    # Implement the logic to start the mixing process
    return "Mixing started"

@app.route('/Cocktail/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            filepath = f"{app.config['UPLOAD_FOLDER']}/{filename}"
            file.save(filepath)
            with open(filepath, newline='') as csvfile:
                reader = csv.reader(csvfile)
                conn = sqlite3.connect('barrobot.db')
                cursor = conn.cursor()
                for row in reader:
                    name = row[0].split(':')[0].strip()
                    ingredients = []
                    total_volumes = []
                    pour_times = []
                    for i in range(1, len(row)):
                        if i % 3 == 1:
                            ingredients.append(row[i].strip())
                        elif i % 3 == 2:
                            total_volumes.append(row[i].strip())
                        elif i % 3 == 0:
                            pour_times.append(row[i].strip())
                    cursor.execute('''
                    INSERT INTO cocktails (name, ingredients, total_volumes, pour_times, image_url)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (name, ', '.join(ingredients), ', '.join(total_volumes), ', '.join(pour_times), row[-1].strip()))
                conn.commit()
                conn.close()
            logger.info('Cocktails uploaded successfully')
            return "Cocktails uploaded successfully"
    return render_template('upload_csv.html')

# Positions routes
@app.route('/positions', methods=['GET'])
def view_positions():
    conn = sqlite3.connect('barrobot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM positions')
    positions = cursor.fetchall()
    conn.close()
    logger.info('Viewing positions')
    return render_template('positions.html', positions=positions)

@app.route('/positions/move_to', methods=['POST'])
def move_to_position():
    position_id = request.json.get('position_id')
    conn = sqlite3.connect('barrobot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT position FROM positions WHERE id = ?', (position_id,))
    position = cursor.fetchone()
    conn.close()
    if position:
        logger.info(f'Moving to position {position_id}')
        stepper.set_current_pos(position[0])
        return f"Moved to position {position[0]}"
    else:
        logger.warning(f'Position {position_id} not found')
        return "Position not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
