from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv


app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')
mongo_uri = os.getenv('MONGODB_URI')
client = MongoClient(mongo_uri)
db = client['agrilink']
farmers_collection = db['farmers']
customers_collection = db['customers']
products_collection = db['products']
orders_collection = db['orders']


# Landing page to select Farmer or Customer
@app.route('/')
def index():
    return render_template('index.html')

# Farmer Signup Route
@app.route('/farmer/signup', methods=['GET', 'POST'])
def farmer_signup():
    if request.method == 'POST':
        farm_name = request.form['farm_name']
        farmer_name = request.form['farmer_name']
        email = request.form['email']
        phone = request.form['phone']
        location = request.form['location']
        password = request.form['password']

        # Create a farmer document to insert into MongoDB
        farmer_data = {
            'farm_name': farm_name,
            'farmer_name': farmer_name,
            'email': email,
            'phone': phone,
            'location': location,
            'password': password
        }

        # Insert farmer data into MongoDB collection
        farmers_collection.insert_one(farmer_data)
        
        return redirect(url_for('farmer_login'))  # Redirect to farmer login after signup
    
    return render_template('farmer_signup.html')

# Customer Signup Route
@app.route('/customer/signup', methods=['GET', 'POST'])
def customer_signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        address = request.form['address']

        # Create a customer document to insert into MongoDB
        customer_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'password': password,
            'address': address
        }

        # Insert customer data into MongoDB collection
        customers_collection.insert_one(customer_data)
        
        return redirect(url_for('customer_login'))  # Redirect to customer login after signup
    
    return render_template('customer_signup.html')

# Farmer Login Route
@app.route('/farmer/login', methods=['GET', 'POST'])
def farmer_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if the farmer exists in the database with the provided email and password
        farmer = farmers_collection.find_one({'email': email, 'password': password})
        
        if farmer:
            # Store farmer details in the session
            session['user_id'] = str(farmer['_id'])
            session['user_type'] = 'farmer'
            session['username'] = farmer['farmer_name']
            # Successful login, redirect to the farmer dashboard
            return redirect(url_for('farmer_dashboard'))
        else:
            # Invalid credentials, show error message
            error = "Invalid email or password"
            return render_template('farmer_login.html', error=error)
    
    return render_template('farmer_login.html')

# Customer Login Route
@app.route('/customer/login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Query MongoDB to find the user by email and password
        user = customers_collection.find_one({'email': email, 'password': password})
        
        if user:
            # Store customer details in the session
            session['user_id'] = str(user['_id'])
            session['user_type'] = 'customer'
            session['username'] = user['first_name']
            # Redirect to customer dashboard (or any other page)
            return redirect(url_for('customer_dashboard'))
        else:
            # If credentials are incorrect, show an error message
            flash('Invalid email or password. Please try again.', 'error')
            return redirect(url_for('customer_login'))

    return render_template('customer_login.html')

# Farmer Dashboard Route
@app.route('/farmer/dashboard')
def farmer_dashboard():
    if 'user_id' in session and session['user_type'] == 'farmer':
        farmer_id = session['user_id']  # Get the farmer's ID from the session
        products = products_collection.find({'farmer_id': ObjectId(farmer_id)})  # Filter by farmer_id
        return render_template('farmer_dashboard.html', products=products)
    return redirect(url_for('farmer_login'))


# Customer Dashboard Route
@app.route('/customer/dashboard', methods=['GET', 'POST'])
def customer_dashboard():
    if 'user_id' in session and session['user_type'] == 'customer':
        selected_category = request.args.get('category')

        # Debugging: Print selected category
        print(f"Selected Category: {selected_category}")

        # Fetch products based on category selection
        if selected_category:
            products = products_collection.find({'category': selected_category})
            # Count products in the selected category
            product_count = products_collection.count_documents({'category': selected_category})
        else:
            products = products_collection.find()  # Fetch all products if no category is selected
            # Count all products
            product_count = products_collection.count_documents({})

        # Debugging: Print the number of products found
        print(f"Products Found: {product_count}")

        categories = products_collection.distinct('category')  # Get distinct categories for the dropdown
        
        product_list = []
        # Fetch farmer details for each product
        for product in products:
            farmer = farmers_collection.find_one({'_id': product['farmer_id']})  # Assuming there's a farmers_collection
            product['farmer_name'] = farmer['farmer_name'] if farmer else 'Unknown'
            product['farmer_location'] = farmer['location'] if farmer else 'Unknown'
            product_list.append(product)

        # Debugging: Print product list
        print(f"Products to Render: {product_list}")

        return render_template('customer_dashboard.html', products=product_list, categories=categories)

    return redirect(url_for('customer_login'))



@app.route('/farmer/add_product', methods=['GET', 'POST'])
def add_product():
    if 'user_id' in session and session['user_type'] == 'farmer':
        farmer = farmers_collection.find_one({'_id': ObjectId(session['user_id'])})
        if not farmer:
            return "Farmer not found", 404

        farmer_name = farmer.get('farmer_name', 'Unknown Farmer')
        farmer_location = farmer.get('location', 'Unknown Location')

        if request.method == 'POST':
            name = request.form['product_name']
            category = request.form['category']
            price = request.form['price']
            price_unit = request.form['price_unit']
            image_url = request.form['image_url']  # Taking URL instead of file

            if not image_url.startswith(("http://", "https://")):
                flash("Invalid image URL. Please provide a valid URL.", "error")
                return redirect(url_for('add_product'))

            product_data = {
                'name': name,
                'category': category,
                'price': f"{price} {price_unit}",
                'image': image_url,  # Storing URL
                'farmer_id': ObjectId(session['user_id']),
                'farmer_name': farmer_name,
                'farmer_location': farmer_location
            }

            products_collection.insert_one(product_data)
            return redirect(url_for('farmer_dashboard'))

        return render_template('farmer_add_product.html', farmer_name=farmer_name, farmer_location=farmer_location)

    return redirect(url_for('farmer_login'))

@app.route('/cart/add/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'user_id' not in session or session['user_type'] != 'customer':
        return redirect(url_for('customer_login'))

    product = products_collection.find_one({'_id': ObjectId(product_id)})
    if not product:
        flash("Product not found!", "error")
        return redirect(url_for('customer_dashboard'))

    quantity = int(request.form.get('quantity', 1))  # Get quantity input from user

    cart_item = {
        'customer_id': ObjectId(session['user_id']),
        'product_id': ObjectId(product_id),
        'farmer_id': product['farmer_id'],
        'product_name': product['name'],
        'category': product['category'],
        'quantity': quantity,
        'price': product['price'],
        'unit': product['price'].split()[-1],  # Extract unit (kg, dozen, litre, etc.)
        'image': product['image'],
        'status': 'Pending'  # Initial status
    }

    orders_collection.insert_one(cart_item)  # Store cart items as orders
    flash("Added to cart!", "success")
    return redirect(url_for('customer_orders'))


@app.route('/customer/orders')
def customer_orders():
    if 'user_id' not in session or session['user_type'] != 'customer':
        return redirect(url_for('customer_login'))

    orders = list(orders_collection.find({'customer_id': ObjectId(session['user_id'])}))
    return render_template('customer_orders.html', orders=orders)


@app.route('/farmer/orders')
def farmer_orders():
    if 'user_id' not in session or session['user_type'] != 'farmer':
        return redirect(url_for('farmer_login'))

    orders = list(orders_collection.find({'farmer_id': ObjectId(session['user_id'])}))

    # Fetch customer details for each order
    for order in orders:
        customer = customers_collection.find_one({'_id': ObjectId(order['customer_id'])})
        order['customer'] = customer  # Add customer details to the order

    return render_template('farmer_orders.html', orders=orders)



@app.route('/order/deliver/<order_id>', methods=['POST'])
def deliver_order(order_id):
    if 'user_id' not in session or session['user_type'] != 'farmer':
        return redirect(url_for('farmer_login'))

    orders_collection.update_one({'_id': ObjectId(order_id)}, {'$set': {'status': 'Delivered'}})
    flash("Order marked as Delivered!", "success")
    return redirect(url_for('farmer_orders'))



@app.route('/customer/profile', methods=['GET', 'POST'])
def customer_profile():
    if 'user_id' not in session or session['user_type'] != 'customer':
        return redirect(url_for('customer_login'))

    customer = customers_collection.find_one({'_id': ObjectId(session['user_id'])})

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        address = request.form['address']

        customers_collection.update_one(
            {'_id': ObjectId(session['user_id'])},
            {'$set': {'first_name': first_name, 'last_name': last_name, 'phone': phone, 'address': address}}
        )

        flash("Profile updated successfully!", "success")
        return redirect(url_for('customer_profile'))

    return render_template('customer_profile.html', customer=customer)



@app.route('/about')
def about():
    return render_template('about.html')
# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
