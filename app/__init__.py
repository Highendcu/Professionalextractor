from flask import Flask
from flask_session import Session
from flask_socketio import SocketIO
from app.extensions import db

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SESSION_TYPE'] = 'filesystem'

    # Initialize extensions
    db.init_app(app)
    Session(app)
    socketio.init_app(app)

    # Register blueprints
    from .routes import main, admin, api
    app.register_blueprint(main.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(api.bp)

    # Pass socketio to extractor
    from app.services.extractor import set_socketio
    set_socketio(socketio)

    # Create database tables
    with app.app_context():
        from app.models import user
        db.create_all()

    return app
