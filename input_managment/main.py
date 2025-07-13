import time
from unittest import result

import requests
from  user_authentication import user_auth 
import pwinput
import working_config
from product_managment import product
from config_management.config import config
from product_managment import sales_management
from product_managment import stock


def handle_input(user_input):
    if working_config.mode == 1:
        if user_input.startswith("update"):
            parts = user_input.split(maxsplit=2)

            if len(parts) < 3:
                print("Invalid Config Update: missing config_option or value")
            else:
                _, config_option, value_str = parts

                if value_str == "True":
                    value = True
                elif value_str == "False":
                    value = False
                elif (value_str.startswith('"') and value_str.endswith('"')) or (
                        value_str.startswith("'") and value_str.endswith("'")):
                    value = value_str[1:-1]
                else:
                    try:
                        if '.' in value_str:
                            value = float(value_str)
                        else:
                            value = int(value_str)
                    except ValueError:
                        value = value_str

                # Actually perform the update
                try:
                    config.update(config_option, value)
                    print(f"Updated '{config_option}' to {value} (type: {type(value).__name__})")
                except AttributeError as e:
                    print(f"Error: {e}")
        elif user_input.startswith("stock"):
            parts = user_input.split(maxsplit=2)

            if len(parts) < 3:
                print("Invalid Stock Update")
            else:
                _, product_name, stock_amount = parts

                stock_status = stock.update_stock(product_name, int(stock_amount))

                if stock_status:
                    print(f"Successfully Updated {product_name}'s Stock to {stock_amount}")


                else:
                    print("Failed to update stock")

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

        elif result == "delete":
            if working_config.mode != 4:
                print("You need to be a manager to delete product!")
                return

            product_name = input("Please Enter Product Name: ")
            product_data = product.delete_product(product_name)
            if product_data == False:
                print("Product Deletion Failed")
                return

            print("Product Deleted Successfully!")

        elif result == "price":

            product_name = input("Please Enter Product Name: ")

            price = product.lookup_price(product_name)

            print(f"{product_name}: {price}")

        elif result == "sale":
            product_name = input("Please Enter Product Name: ")
            quantity = input("Please Enter Quantity: ")
            quantity = int(quantity)

            status = sales_management.register_sale(product_name, quantity)

            if status == False:
                print("Sale Creation Failed")
                return

            print("Product Created")

        elif result == "profits":
            print("Fetching Profit Report!")

            profit_report = sales_management.get_sales_report()

            print(f"Total Revenue: ${profit_report['total_revenue']}")

        elif result == "stock":
            product_name = input("Please Enter Product Name: ")

            amount_of_stock = stock.get_stock(product_name)

            print(f"{product_name}'s Stock is {amount_of_stock}")

        else:
            print("Invalid Subcommand")

