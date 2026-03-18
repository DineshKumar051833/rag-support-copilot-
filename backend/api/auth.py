import json
from pathlib import Path

USERS_FILE = Path("data/users.json")


def load_users():
    if not USERS_FILE.exists():
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def signup_user(username, password):
    users = load_users()

    # check if user exists
    for user in users:
        if user["username"] == username and user["password"] == password:
            return False, "User already exists"

    users.append({
        "username": username,
        "password": password
    })

    save_users(users)
    return True, "User created successfully"


def login_user(username, password):
    users = load_users()

    for user in users:
        if user["username"] == username and user["password"] == password:
            return True, "Login successful"

    return False, "Invalid credentials"
