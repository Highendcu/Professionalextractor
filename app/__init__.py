from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

socketio = SocketIO()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')
    db.init_app(app)
    socketio.init_app(app)

    # ⬇️ Move imports AFTER app is created
    from .routes.main import bp as main
    from .routes.admin import admin
    from .routes.api import api

    # ⬇️ Register blueprints with app
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(api)

    return app
