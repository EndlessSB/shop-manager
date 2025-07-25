import time
import json
from datetime import datetime
import os
from config_management.config import config
from discord_intergration import discord
from product_managment import stock

products_data = "products.json"

if os.path.exists(products_data):
    with open(products_data, "r") as file:
        try:
            products = json.load(file)
            if not isinstance(products, list):
                raise ValueError("Expected a list at the root of products.json")
        except json.JSONDecodeError:
            products = []  # File exists but is empty or corrupt
else:
    products = []  # File doesn't exist yet


# Get product
def get_product(product_name):
    product_data = next((u for u in products if u.get("item_name") == product_name), None)
    return product_data  # You don't need the extra if-check


def create_product(product_name, price):
    product_data = {
        "item_name": product_name,
        "price": price,
        "creation_date": datetime.now().isoformat()  # ISO format datetime string
    }

    products.append(product_data)
    try:
        with open(products_data, "w") as file:
            json.dump(products, file, indent=4)

        if config.discord_integration_status:
            discord.product_create_alert(product_name, price)
        
        stock.sync_all_products_into_stock() # More logical Place then previously

        return True
    except Exception as e:
        print(e)  # Probably should add more comprehensive error reporting later.
        return False

def lookup_price(product_name):
    products_data = get_product(product_name)

    if not products_data:
        return 0

    return float(products_data["price"])

def delete_product(product_name):
    global products  # Need to modify the global list

    product = get_product(product_name)
    if not product:
        print(f"Product '{product_name}' not found.")
        return False

    products = [p for p in products if p.get("item_name") != product_name]

    try:
        with open(products_data, "w") as file:
            json.dump(products, file, indent=4)
        print(f"Product '{product_name}' deleted.")
        return True
    except Exception as e:
        print(f"Error deleting product: {e}")
        return False

def get_all_products():
    return products
