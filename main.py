# Write your code here :
import time as t
import random as r

import pwinput

import input_managment.main
import working_config
from user_authentication import user_auth
import web_ui
import threading
from product_managment import stock

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


if __name__ == "__main__":
    # Start web UI thread
    web_thread = threading.Thread(target=web_ui.run_web)
    web_thread.daemon = True
    web_thread.start()

    # Get and print IP

    # Fancy ASCII banner
    print(r"""
  ____  _                 __  __                                    
 / ___|| |__   ___  _ __ |  \/  | __ _ _ __   __ _  __ _  ___ _ __ 
 \___ \| '_ \ / _ \| '_ \| |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
  ___) | | | | (_) | |_) | |  | | (_| | | | | (_| | (_| |  __/ |   
 |____/|_| |_|\___/| .__/|_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|   
                   |_|                             |___/           
    """)

    print(f"[ Web UI running at: http://127.0.0.1:5000 ]\n")
    print("=" * 60)
    print("LOGIN")
    print("=" * 60)

    username = input("Username: ")
    password = pwinput.pwinput("Password: ")

    login_status = user_auth.login(username, password)

    if login_status:
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        # Syncing Stock
        stock.sync_all_products_into_stock()
        while True:
            user_input = input(f"{mode_to_text(working_config.mode)} | --> ")
            if user_input == "exit":
                exit()
            input_managment.main.handle_input(user_input)
    else:
        print("Invalid Username or Password")
        exit()