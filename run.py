from app import create_app
import os

app, socketio = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    print(f"[INFO] Running on port {port} with eventlet")
    socketio.run(app, host='0.0.0.0', port=port)
