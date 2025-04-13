### app/services/validator.py
from datetime import datetime
from app.models.user import load_users

def validate_credentials(username, password):
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            expiry = user.get("expiry")
            if not expiry or datetime.fromisoformat(expiry) > datetime.utcnow():
                return True, "Valid license"
            else:
                return False, "License expired"
    return False, "Invalid credentials"


def is_license_expired(user):
    expiry = user.get("expiry")
    if not expiry:
        return False
    return datetime.fromisoformat(expiry) < datetime.utcnow()