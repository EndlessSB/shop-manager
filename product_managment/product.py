import time
import json
from datetime import datetime
import os


products_data = "products.json"

# Load or initialize the users table (a list)
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

        return True
    except Exception as e:
        print(e)  # Probably should add more comprehensive error reporting later.
        return False

def lookup_price(product_name):
    products_data = get_product(product_name)

    if not products_data:
        return 0

    return float(products_data["price"])

