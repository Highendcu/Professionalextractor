from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

socketio = SocketIO()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')
    db.init_app(app)
    socketio.init_app(app)

    # ⬇️ Move imports AFTER app is created
    from .routes.main import bp as main
    from .routes.admin import bp as admin
    from .routes.api import bp as api

    # ⬇️ Register blueprints with app
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(api)

    return app
