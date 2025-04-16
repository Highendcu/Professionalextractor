# app/__init__.py
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../config.py")

    from app.services.extractor import set_socketio
    set_socketio(socketio)

    CORS(app)
    socketio.init_app(app)

    from .routes import main, admin, api
    app.register_blueprint(main.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(api.bp)

    return app
