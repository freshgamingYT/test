import json
import logging
from flask import request, render_template, redirect, url_for

logger = logging.getLogger()

def init_routes(app, stepper, servo, scale, cocktail):
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
        try:
            cocktail_name = request.args.get('cocktail_name')
            cocktail_data = cocktail.select(cocktail_name)
            if isinstance(cocktail_data, dict):
                return render_template('c1.html', cocktail=cocktail_data)
            else:
                return "Cocktail not found", 404
        except Exception as e:
            logger.error(f"Error displaying cocktail info: {e}")
            return "Internal Server Error", 500

    # Servo routes
    @app.route('/servo/init', methods=['GET'])
    def init_servo():
        """
        Initialize the servo motor.
        """
        try:
            logger.info('Initializing servo motor')
            return servo.init()
        except Exception as e:
            logger.error(f"Error initializing servo motor: {e}")
            return "Internal Server Error", 500

    @app.route('/servo/enable', methods=['POST'])
    def enable_servo():
        """
        Enable the servo motor.
        """
        try:
            logger.info('Enabling servo motor')
            return servo.enable()
        except Exception as e:
            logger.error(f"Error enabling servo motor: {e}")
            return "Internal Server Error", 500

    @app.route('/servo/disable', methods=['POST'])
    def disable_servo():
        """
        Disable the servo motor.
        """
        try:
            logger.info('Disabling servo motor')
            return servo.disable()
        except Exception as e:
            logger.error(f"Error disabling servo motor: {e}")
            return "Internal Server Error", 500

    # Scale routes
    @app.route('/scale/init', methods=['GET'])
    def init_scale():
        """
        Initialize the scale.
        """
        try:
            logger.info('Initializing scale')
            return scale.init()
        except Exception as e:
            logger.error(f"Error initializing scale: {e}")
            return "Internal Server Error", 500

    @app.route('/scale/calibrate_scale', methods=['POST'])
    def calibrate_scale():
        """
        Calibrate the scale.
        """
        try:
            logger.info('Calibrating scale')
            return scale.calibrate()
        except Exception as e:
            logger.error(f"Error calibrating scale: {e}")
            return "Internal Server Error", 500

    @app.route('/scale/enable', methods=['POST'])
    def enable_scale():
        """
        Enable the scale.
        """
        try:
            logger.info('Enabling scale')
            return scale.enable()
        except Exception as e:
            logger.error(f"Error enabling scale: {e}")
            return "Internal Server Error", 500

    @app.route('/scale/disable', methods=['POST'])
    def disable_scale():
        """
        Disable the scale.
        """
        try:
            logger.info('Disabling scale')
            return scale.disable()
        except Exception as e:
            logger.error(f"Error disabling scale: {e}")
            return "Internal Server Error", 500

    # Cocktail routes
    @app.route('/cocktail/select_cocktail', methods=['POST'])
    def select_cocktail():
        """
        Select a cocktail and redirect to its details page.
        """
        try:
            cocktail_name = request.json.get('cocktail')
            cocktail_data = cocktail.select(cocktail_name)
            if isinstance(cocktail_data, dict):
                logger.info(f'Selected cocktail {cocktail_name}')
                return redirect(url_for('show_cocktail', cocktail_name=cocktail_name))
            else:
                logger.warning(f'Cocktail {cocktail_name} not found')
                return cocktail_data
        except Exception as e:
            logger.error(f"Error selecting cocktail: {e}")
            return "Internal Server Error", 500

    @app.route('/cocktail/show/<cocktail_name>', methods=['GET'])
    def show_cocktail(cocktail_name):
        """
        Show the details of a selected cocktail.
        """
        try:
            cocktail_data = cocktail.select(cocktail_name)
            if isinstance(cocktail_data, dict):
                logger.info(f'Showing details for cocktail {cocktail_name}')
                return render_template('cocktail.html', cocktail=cocktail_data)
            else:
                logger.warning(f'Cocktail {cocktail_name} not found')
                return "Cocktail not found", 404
        except Exception as e:
            logger.error(f"Error showing cocktail details: {e}")
            return "Internal Server Error", 500

    @app.route('/cocktail/start_mixing', methods=['POST'])
    def start_mixing():
        """
        Start the mixing process for the selected cocktail.
        """
        try:
            logger.info('Starting mixing process')
            # Implement the logic to start the mixing process
            return "Mixing started"
        except Exception as e:
            logger.error(f"Error starting mixing process: {e}")
            return "Internal Server Error", 500

    @app.route('/cocktail/upload_csv', methods=['GET', 'POST'])
    def upload_csv():
        """
        Upload a CSV file containing cocktail recipes.
        """
        if request.method == 'POST':
            try:
                file = request.files['file']
                if file and file.filename.endswith('.csv'):
                    filename = secure_filename(file.filename)
                    filepath = f"{app.config['UPLOAD_FOLDER']}/{filename}"
                    file.save(filepath)
                    with open(filepath, newline='') as csvfile:
                        reader = csv.reader(csvfile)
                        with open('data.json', 'r') as json_file:
                            data = json.load(json_file)
                        for row in reader:
                            name = row[0]
                            ingredients = [row[1], row[3], row[5]]
                            pour_times = [row[2], row[4], row[6]]
                            image_url = row[7]
                            data['cocktails'].append({
                                'name': name,
                                'ingredients': ', '.join(ingredients),
                                'total_volumes': ', '.join(pour_times),
                                'pour_times': ', '.join(pour_times),
                                'image_url': image_url
                            })
                        with open('data.json', 'w') as json_file:
                            json.dump(data, json_file, indent=4)
                    logger.info('Cocktails uploaded successfully')
                    return "Cocktails uploaded successfully"
            except Exception as e:
                logger.error(f"Error uploading CSV: {e}")
                return "Internal Server Error", 500
        return render_template('upload_csv.html')

     # Positions routes
    @app.route('/positions', methods=['GET'])
    def view_positions():
        """
        View the positions stored in the data file.
        """
        try:
            with open('data.json', 'r') as json_file:
                data = json.load(json_file)
            positions = data['positions']
            logger.info('Viewing positions')
            return render_template('positions.html', positions=positions)
        except Exception as e:
            logger.error(f"Error viewing positions: {e}")
            return "Internal Server Error", 500

    @app.route('/positions/move_to', methods=['POST'])
    def move_to_position():
        """
        Move the stepper motor to a specified position.
        """
        try:
            position_id = request.json.get('position_id')
            with open('data.json', 'r') as json_file:
                data = json.load(json_file)
            position = next((pos for pos in data['positions'] if pos['id'] == position_id), None)
            if position:
                logger.info(f'Moving to position {position_id}')
                stepper.set_current_pos(position['position'])
                return f"Moved to position {position['position']}"
            else:
                logger.warning(f'Position {position_id} not found')
                return "Position not found", 404
        except Exception as e:
            logger.error(f"Error moving to position: {e}")
            return "Internal Server Error", 500
