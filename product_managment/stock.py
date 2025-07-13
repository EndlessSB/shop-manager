import time as t
import json
import os
from datetime import datetime
from product_managment import product  # Assuming it's imported correctly


stock_data = "stock.json"

# Load or initialize the users table (a list)
if os.path.exists(stock_data):
    with open(stock_data, "r") as file:
        try:
            stock = json.load(file)
            if not isinstance(stock, list):
                raise ValueError("Expected a list at the root of products.json")
        except json.JSONDecodeError:
            stock = []  # File exists but is empty or corrupt
else:
    stock = []  # File doesn't exist yet



# Get stock data via product name
def get_stock_data(product_name):
    sotck_d = next((u for u in stock if u.get("item_name") == product_name), None)
    return sotck_d  


def add_product_stock(product_name, price, stock):
    product_data = {
        "item_name": product_name,
        "cost": price,
        "stock": stock,
        "creation_date": datetime.now().isoformat()  # ISO format datetime string
    }

    stock.append(product_data)
    try:
        with open(stock_data, "w") as file:
            json.dump(stock, file, indent=4)

        return True
    except Exception as e:
        print(e)  # Probably should add more comprehensive error reporting later.
        return False

def sync_all_products_into_stock():
    global stock  # So we can modify the list
    existing_item_names = {item.get("item_name") for item in stock}

    new_entries_added = 0
    for p in product.get_all_products():
        name = p.get("item_name")
        if name not in existing_item_names:
            new_stock_entry = {
                "item_name": name,
                "cost": 0,  # Default cost
                "stock": 0,  # Default stock
                "creation_date": datetime.now().isoformat()
            }
            stock.append(new_stock_entry)
            new_entries_added += 1

    if new_entries_added > 0:
        try:
            with open(stock_data, "w") as file:
                json.dump(stock, file, indent=4)
            print(f"Synced {new_entries_added} products into stock.")
        except Exception as e:
            print(f"Failed to sync stock: {e}")
    else:
        print("Stock already in sync with products.")



def update_stock(item_name, new_stock):
    stocks = get_stock_data(item_name)
    if not stocks:
        return False
    
    stocks['stock'] = new_stock

    try:
        with open(stock_data, "w") as file:
            json.dump(stock, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False
    
def update_cost(item_name, new_cost):
    stocks = get_stock_data(item_name)
    if not stocks:
        return False
    
    stocks['cost'] = new_cost

    try:
        with open(stock_data, "w") as file:
            json.dump(stock, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False
def get_cost(item_name):
    stocks = get_stock_data(item_name)

    if stocks is None or 'cost' not in stocks:
        return 0

    return stocks['cost']

def get_stock(item_name):
    stocks = get_stock_data(item_name)

    if stocks is None or 'stock' not in stocks:
        return 0

    return stocks['stock']
