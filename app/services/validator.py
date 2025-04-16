import json
import os
from datetime import datetime

USERS_FILE = os.path.join("app", "data", "users.json")

def validate_credentials(username, password):
    if not os.path.exists(USERS_FILE):
        return False, "User database not found"

    try:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    except json.JSONDecodeError:
        return False, "Invalid user data"

    for user in users:
        if user.get("username") == username and user.get("password") == password:
            expiry = user.get("expiry")
            if expiry:
                try:
                    expiry_date = datetime.fromisoformat(expiry)
                    if expiry_date < datetime.utcnow():
                        return False, "License expired"
                except Exception:
                    return False, "Invalid expiry format"
            return True, "Valid credentials"
    
    return False, "Invalid username or password"