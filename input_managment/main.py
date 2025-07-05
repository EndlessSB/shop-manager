import time
import requests
from  user_authentication import user_auth 
import pwinput
import config


def handle_input(user_input):
    if user_input.startswith("mode"):
        parts = user_input.split("mode", 1)
        result = parts[1].strip() if len(parts) > 1 else ""

        if result == "":
            print("Invalid Mode")
        
        elif result == "manager":
            username = input("Please Enter your Username: ")
            password = pwinput.pwinput(prompt="Enter password: ")

            login_status = user_auth.login(username, password)

            if login_status == True:
                role = user_auth.username_to_role(username)

                if role == "manager":
                    config.mode = 4
                    print("Auth Successful")
                else:
                    print("Auth Failed")

            else:
                print("Invalid Username Or Pass")

