import json
import os
from datetime import datetime
from product_managment.product import get_product
from product_managment import stock

sales_log_path = "sales.json"

# Ensure the sales file exists
if not os.path.exists(sales_log_path):
    with open(sales_log_path, "w") as f:
        json.dump([], f)

def register_sale(product_name, quantity):
    product = get_product(product_name)
    if not product:
        print(f"Product '{product_name}' not found.")
        return False

    try:
        price = float(product["price"])
        total = round(price * quantity, 2)

        sale_entry = {
            "product": product_name,
            "quantity": quantity,
            "price": price,
            "total": total,
            "timestamp": datetime.now().isoformat()
        }

        # Load and append
        with open(sales_log_path, "r") as f:
            sales = json.load(f)

        sales.append(sale_entry)

        with open(sales_log_path, "w") as f:
            json.dump(sales, f, indent=4)

        print(f"Registered sale: {quantity} x {product_name} = ${total}")
        return True
    except Exception as e:
        print(f"Error registering sale: {e}")
        return False


def get_sales_report():
    if not os.path.exists(sales_log_path):
        return {}

    with open(sales_log_path, "r") as f:
        sales = json.load(f)

    report = {
        "products": {},
        "total_revenue": 0.0,
        "total_cost": 0.0,
        "total_profit": 0.0
    }

    for sale in sales:
        product = sale["product"]
        total = sale["total"]
        quantity = sale["quantity"]

        # Get cost per unit
        unit_cost = stock.get_cost(product)
        total_cost = unit_cost * quantity
        profit = total - total_cost

        if product not in report["products"]:
            report["products"][product] = {
                "quantity": 0,
                "revenue": 0.0,
                "cost": 0.0,
                "profit": 0.0
            }

        report["products"][product]["quantity"] += quantity
        report["products"][product]["revenue"] += total
        report["products"][product]["cost"] += total_cost
        report["products"][product]["profit"] += profit

        report["total_revenue"] += total
        report["total_cost"] += total_cost
        report["total_profit"] += profit

    return report


