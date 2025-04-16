from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from .services.extractor import set_socketio

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SECRET_KEY'] = 'your-secret-key'
	
	socketio.init_app(app)

    # blueprints here
    from app.routes.admin import admin as admin_blueprint
    from app.routes.api import api as api_blueprint
    from app.routes.main import main as main_blueprint

    app.register_blueprint(admin_blueprint)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(main_blueprint)

    return app, socketio