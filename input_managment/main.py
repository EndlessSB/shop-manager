import time
from unittest import result

import requests
from  user_authentication import user_auth 
import pwinput
import working_config
from product_managment import product


def handle_input(user_input):
    if working_config.mode == 1:
        if user_input.startswith("update"):
            parts = user_input.split(maxsplit=2)  # split into at most 3 parts: "update", "config_option", "value"

            if len(parts) < 3:
                print("Invalid Config Update: missing config_option or value")
            else:
                _, config_option, value_str = parts

                # Check if value is boolean (True/False without quotes)
                if value_str == "True":
                    value = True
                elif value_str == "False":
                    value = False
                # Check if value is quoted string
                elif (value_str.startswith('"') and value_str.endswith('"')) or (
                        value_str.startswith("'") and value_str.endswith("'")):
                    # strip quotes
                    value = value_str[1:-1]
                else:
                    # Optional: try to convert to int or float, otherwise keep as string
                    try:
                        if '.' in value_str:
                            value = float(value_str)
                        else:
                            value = int(value_str)
                    except ValueError:
                        value = value_str  # fallback to string

                # Now you have config_option and value correctly typed
                print(f"Updating config option '{config_option}' to value: {value} (type: {type(value).__name__})")


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
                    working_config.mode = 4
                    print("Auth Successful")
                else:
                    print("Auth Failed")

            else:
                print("Invalid Username Or Pass")

        elif result == "config":
            working_config.mode = 1

            print("Mode Set to config!")
    if user_input.startswith("product"):
        parts = user_input.split("product", 1)
        result = parts[1].strip() if len(parts) > 1 else ""

        if result == "":
            print("Invalid Product")

        if result == "create":
            if working_config.mode != 4:
                print("You need to be a manager to create product!")
                return

            product_name = input("Please Enter Product Name: ")
            price = input("Please Enter Price: ")

            product_data = product.create_product(product_name, price)

            if product_data == False:
                print("Product Creation Failed")
            else:
                print("Product Created")

        elif result == "price":

            product_name = input("Please Enter Product Name: ")

            price = product.lookup_price(product_name)

            print(f"{product_name}: {price}")

        else:
            print("Invalid Subcommand")



    else:
        print("Invalid Input")