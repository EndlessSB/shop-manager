# Write your code here :
import time as t
import random as r
import input_managment.main
import config


## Basic Mode Management

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

while True:
    user_input = input(f"{mode_to_text(config.mode)} | --> ")

    input_managment.main.handle_input(user_input)