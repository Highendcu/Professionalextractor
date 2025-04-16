from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key'
    CORS(app)
    
    from app.routes.main import bp as main
    from app.routes.admin import admin
    from app.routes.api import bp as api

    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(api)

    from app.services.extractor import set_socketio
    set_socketio(socketio)

    return app
