from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import logging
import sys
import os
from config_management import config

from user_authentication import user_auth
from product_managment import product
from product_managment import sales_management

app = Flask(__name__)
app.secret_key = os.urandom(32)  # Replace with a secure key in production

# Hide startup banner
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

# ========== 🔐 AUTH ROUTES ==========

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if user_auth.login(username, password):
            session['username'] = username
            session['role'] = user_auth.username_to_role(username)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ========== 🔐 AUTH CHECK ==========

def is_authenticated():
    return 'username' in session

def require_login():
    if not is_authenticated():
        return redirect(url_for('login'))

# ========== 🧠 MAIN DASHBOARD ==========

@app.route('/')
def dashboard():
    if not is_authenticated():
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

@app.route('/products')
def products_page():
    if not is_authenticated():
        return redirect(url_for('login'))
    return render_template('products.html')


@app.route('/sales')
def sales_page():
    if not is_authenticated():
        return redirect(url_for('login'))
    return render_template('sales.html')


@app.route('/pos')
def pos_page():
    if not is_authenticated():
        return redirect(url_for('login'))

    all_products = product.get_all_products()
    return render_template('pos.html', products=all_products)


# ========== 📦 PRODUCT ROUTES ==========

@app.route('/products/create', methods=['POST'])
def create_product():
    if not is_authenticated() or session['role'] != 'manager':
        return "Unauthorized", 403

    data = request.form
    name = data.get("name")
    price = data.get("price")

    if not name or not price:
        return "Missing name or price", 400

    success = product.create_product(name, price)
    if success:
        return "Product created", 200
    return "Product creation failed", 500

@app.route('/products/delete', methods=['POST'])
def delete_product():
    if not is_authenticated() or session['role'] != 'manager':
        return "Unauthorized", 403

    name = request.form.get("name")
    if not name:
        return "Missing name", 400

    success = product.delete_product(name)
    if success:
        return "Deleted", 200
    return "Delete failed", 500

@app.route('/products/price/<product_name>')
def get_price(product_name):
    if not is_authenticated():
        return redirect(url_for('login'))

    price = product.lookup_price(product_name)
    return jsonify({"product": product_name, "price": price})

# ========== 💵 SALES ROUTES ==========

@app.route('/sales/create', methods=['POST'])
def create_sale():
    if not is_authenticated():
        return redirect(url_for('login'))

    data = request.form
    product_name = data.get("product")
    quantity = data.get("quantity")

    try:
        quantity = int(quantity)
    except ValueError:
        return "Invalid quantity", 400

    success = sales_management.register_sale(product_name, quantity)
    if success:
        return "Sale recorded", 200
    return "Sale failed", 500

@app.route('/sales/report')
def get_sales_report():
    if not is_authenticated():
        return redirect(url_for('login'))

    report = sales_management.get_sales_report()
    return jsonify(report)

# ========== 🧪 TEST ROUTE ==========

@app.route('/whoami')
def whoami():
    if not is_authenticated():
        return jsonify({"auth": False})
    return jsonify({
        "username": session['username'],
        "role": session['role']
    })

# ========== 🔁 WEB SERVER ENTRY ==========

def run_web():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
