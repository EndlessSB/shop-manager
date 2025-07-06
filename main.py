# Write your code here :
import time as t
import random as r

import pwinput

import input_managment.main
import working_config
from user_authentication import user_auth


# Managing modes [This is so cooked]
def mode_to_text(mode):
    if mode == 0:
        return "Default"
    elif mode == 1:
        return "config"
    elif mode == 2:
        return "sales"
    elif mode == 3:
        return "refund"
    elif mode == 4:
        return "manager"
    else:
        return "broken"

print("Welcome to the POS system!")

print("")
print("")

print("Login")
print("")
username = input("Please Enter your Username: ")
password = pwinput.pwinput(prompt="Enter your Password: ")

login_status = user_auth.login(username, password)

if login_status:
    while True:
        user_input = input(f"{mode_to_text(working_config.mode)} | --> ")

        input_managment.main.handle_input(user_input)
else:
    print("Invalid Username or Password")
    exit()