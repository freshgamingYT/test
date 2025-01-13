from flask import Blueprint, render_template, request, jsonify
from stepper.positions import PositionManager

cocktail_route = Blueprint('cocktail_route', __name__)
main_route = Blueprint('main_route', __name__)

position_manager = PositionManager('../files/positions.json')

@cocktail_route.route('/1', methods=['GET'])
def cocktail():
    return render_template('C1.html')

@cocktail_route.route('/start', methods=['POST'])
def start():
    data = request.get_json()
    if data['button'] == 'start':
        position_manager.load_positions()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'failed'})

@main_route.route('/', methods=['GET'])
def index():
    return render_template('index.html')

def register_routes(app):
    app.register_blueprint(cocktail_route, url_prefix="/cocktail")
    app.register_blueprint(main_route, url_prefix="/")
