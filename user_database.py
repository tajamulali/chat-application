import hashlib
import os

USER_DATABASE_FILE = 'users.txt'

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    """Register a new user by saving the username and hashed password to the database."""
    if os.path.exists(USER_DATABASE_FILE):
        with open(USER_DATABASE_FILE, 'r') as f:
            for line in f.readlines():
                db_username, _ = line.strip().split(',')
                if db_username == username:
                    return False, "Username already exists!"
    
    with open(USER_DATABASE_FILE, 'a') as f:
        f.write(f"{username},{hash_password(password)}\n")
    return True, "Registration successful!"

def validate_user(username, password):
    """Validate user login by checking the hashed password in the database."""
    if not os.path.exists(USER_DATABASE_FILE):
        return False, "No registered users found."
    
    with open(USER_DATABASE_FILE, 'r') as f:
        for line in f.readlines():
            db_username, db_password = line.strip().split(',')
            if db_username == username and db_password == hash_password(password):
                return True, "Login successful!"
    return False, "Invalid username or password."
