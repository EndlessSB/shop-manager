import time
import requests
from  user_authentication import user_auth 
import pwinput
import config
from product_managment import product


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
    if user_input.startswith("product"):
        parts = user_input.split("product", 1)
        result = parts[1].strip() if len(parts) > 1 else ""

        if result == "":
            print("Invalid Product")

        if result == "create":
            if config.mode != 4:
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