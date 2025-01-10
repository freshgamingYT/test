import argparse
import csv
import json
import logging
import sqlite3
import shutil
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
    pins=[config['step_pin'], config['direction_pin'], config['enable_pin']],
    delay_between_steps=config['us_delay'] * config['uS'],
    left_button_pin=config['servo_steps']['pos1'],
    right_button_pin=config['servo_steps']['pos10']
)
servo = Servo()
scale = Scale()
cocktail = Cocktail()

# Set initial states based on command-line arguments
if args.disable_servo:
    servo.disable()

if args.disable_scale:
    scale.disable()

def backup_db():
    """
    Back up the database to a file.
    """
    try:
        shutil.copy('barrobot.db', 'barrobot_backup.db')
        logger.info("Database backup successful.")
    except Exception as e:
        logger.error(f"Error backing up database: {e}")

def restore_db():
    """
    Restore the database from a backup file.
    """
    try:
        shutil.copy('barrobot_backup.db', 'barrobot.db')
        logger.info("Database restore successful.")
    except Exception as e:
        logger.error(f"Error restoring database: {e}")

# Restore the database when initializing
restore_db()

@app.route('/')
def index():
    """
    Render the main page of the application.
    """
    return render_template('index.html')

@app.route('/bierinfo')
def bierinfo():
    """
    Display the ingredients of the selected cocktail.
    """
    cocktail_name = request.args.get('cocktail_name')
    cocktail_data = cocktail.select(cocktail_name)
    if isinstance(cocktail_data, dict):
        return render_template('c1.html', cocktail=cocktail_data)
    else:
        return "Cocktail not found", 404

# Servo routes
@app.route('/servo/init', methods=['GET'])
def init_servo():
    """
    Initialize the servo motor.
    """
    logger.info('Initializing servo motor')
    return servo.init()

@app.route('/servo/enable', methods=['POST'])
def enable_servo():
    """
    Enable the servo motor.
    """
    logger.info('Enabling servo motor')
    return servo.enable()

@app.route('/servo/disable', methods=['POST'])
def disable_servo():
    """
    Disable the servo motor.
    """
    logger.info('Disabling servo motor')
    return servo.disable()

# Scale routes
@app.route('/scale/init', methods=['GET'])
def init_scale():
    """
    Initialize the scale.
    """
    logger.info('Initializing scale')
    return scale.init()

@app.route('/scale/calibrate_scale', methods=['POST'])
def calibrate_scale():
    """
    Calibrate the scale.
    """
    logger.info('Calibrating scale')
    return scale.calibrate()

@app.route('/scale/enable', methods=['POST'])
def enable_scale():
    """
    Enable the scale.
    """
    logger.info('Enabling scale')
    return scale.enable()

@app.route('/scale/disable', methods=['POST'])
def disable_scale():
    """
    Disable the scale.
    """
    logger.info('Disabling scale')
    return scale.disable()

# Cocktail routes
@app.route('/cocktail/select_cocktail', methods=['POST'])
def select_cocktail():
    """
    Select a cocktail and redirect to its details page.
    """
    cocktail_name = request.json.get('cocktail')
    cocktail_data = cocktail.select(cocktail_name)
    if isinstance(cocktail_data, dict):
        logger.info(f'Selected cocktail {cocktail_name}')
        return redirect(url_for('show_cocktail', cocktail_name=cocktail_name))
    else:
        logger.warning(f'Cocktail {cocktail_name} not found')
        return cocktail_data

@app.route('/cocktail/show/<cocktail_name>', methods=['GET'])
def show_cocktail(cocktail_name):
    """
    Show the details of a selected cocktail.
    """
    cocktail_data = cocktail.select(cocktail_name)
    if isinstance(cocktail_data, dict):
        logger.info(f'Showing details for cocktail {cocktail_name}')
        return render_template('cocktail.html', cocktail=cocktail_data)
    else:
        logger.warning(f'Cocktail {cocktail_name} not found')
        return "Cocktail not found", 404

@app.route('/cocktail/start_mixing', methods=['POST'])
def start_mixing():
    """
    Start the mixing process for the selected cocktail.
    """
    logger.info('Starting mixing process')
    # Implement the logic to start the mixing process
    return "Mixing started"

@app.route('/cocktail/upload_csv', methods=['GET', 'POST'])
def upload_csv():
    """
    Upload a CSV file containing cocktail recipes.
    """
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
                    name = row[0]
                    ingredients = [row[1], row[3], row[5]]
                    pour_times = [row[2], row[4], row[6]]
                    image_url = row[7]
                    cursor.execute('''
                    INSERT INTO cocktails (name, ingredients, total_volumes, pour_times, image_url)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (name, ', '.join(ingredients), ', '.join(pour_times), image_url))
                conn.commit()
                conn.close()
            logger.info('Cocktails uploaded successfully')
            return "Cocktails uploaded successfully"
    return render_template('upload_csv.html')

# Positions routes
@app.route('/positions', methods=['GET'])
def view_positions():
    """
    View the positions stored in the database.
    """
    conn = sqlite3.connect('barrobot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM positions')
    positions = cursor.fetchall()
    conn.close()
    logger.info('Viewing positions')
    return render_template('positions.html', positions=positions)

@app.route('/positions/move_to', methods=['POST'])
def move_to_position():
    """
    Move the stepper motor to a specified position.
    """
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
    try:
        app.run(host='
