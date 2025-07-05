import time
import requests
import os
import bcrypt
from datetime import datetime
import json
### NOTICE ###
# Probably should not be using JSON and for proper implementation probably wouldn't 
# But it might never be changed so be warned !!! 
# BIG SCARY SECURIATY VUNREBILITY !!!!!!!!! [In all seriousness, please never use json like this in prod, I will hunt your ass down and make you refractor your whole code base :))))))]
### NOTICE ###


accounts_data = "accounts.json"

# Load or initialize the users table (a list)
if os.path.exists(accounts_data):
    with open(accounts_data, "r") as file:
        try:
            users = json.load(file)
            if not isinstance(users, list):
                raise ValueError("Expected a list at the root of users.json")
        except json.JSONDecodeError:
            users = []  # File exists but is empty or corrupt
else:
    users = []  # File doesn't exist yet


# I don't even know why this function exsists, Convenience Ig | Probaly not the smartest thing But thats a future me Problem :)
def get_user(username):
    user = next((u for u in users if u.get("name") == username), None)
    if not user:
        return None
    
    return user

def create_user(username, password, role):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    user_data = {
        "name": username,
        "password": hashed_password.decode(),  # store as string for JSON
        "role": role,
        "creation_date": datetime.now().isoformat()  # ISO format datetime string
    }


    users.append(user_data)
    try:
        with open(accounts_data, "w") as file:
            json.dump(users, file, indent=4)
        
        return True
    except Exception as e:
        print(e) # Probably should add more comprehensive error reporting later.
        return False

# Login Function | Self Explanatory
def login(username, password):
    user = get_user(username)
    if not user:
        return False
    
    stored_hash = user.get("password")
    if not stored_hash:
        return False

    # bcrypt needs bytes
    return bcrypt.checkpw(password.encode(), stored_hash.encode())

# Saves me revamping the login Function iswtg.
def username_to_role(username):
    user = get_user(username)
    if not user:
        return None

    role = user.get("role")

    if not role:
        return None
    
    return role

def update_role(username, new_role):
    user = get_user(username)
    if not user:
        return False

    user['role'] = new_role

    try:
        with open(accounts_data, "w") as file:
            json.dump(users, file, indent=4)
        # print(f"Updated role for {username} to {new_role}") # Unquote in case of desperately needing to debug
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False
    
    

