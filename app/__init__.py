from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

socketio = None  # Placeholder

def create_app():
    global socketio  # Let us modify the global socketio object
    app = Flask(__name__)
    app.secret_key = 'your-secret-key'
    CORS(app)

    from app.routes.main import bp as main
    from app.routes.admin import admin
    from app.routes.api import bp as api

    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(api, url_prefix="/api")

    socketio = SocketIO(app, cors_allowed_origins="*")  # Initialize with app

    from app.services.extractor import set_socketio
    set_socketio(socketio)

    return app
