from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Directory to save uploaded images
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.secret_key = os.getenv('SECRET_KEY')
mongo_uri = os.getenv('MONGODB_URI')
client = MongoClient(mongo_uri)
db = client['agrilink']
farmers_collection = db['farmers']
customers_collection = db['customers']
products_collection = db['products']

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

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/farmer/add_product', methods=['GET', 'POST'])
def add_product():
    if 'user_id' in session and session['user_type'] == 'farmer':
        # Fetch the farmer's details from the database
        farmer = farmers_collection.find_one({'_id': ObjectId(session['user_id'])})

        if not farmer:
            return "Farmer not found", 404

        # Get farmer details
        farmer_name = farmer.get('farmer_name', 'Unknown Farmer')
        farmer_location = farmer.get('location', 'Unknown Location')

        if request.method == 'POST':
            name = request.form['product_name']
            category = request.form['category']
            price = request.form['price']
            price_unit = request.form['price_unit']  # Added this to capture price unit
            image = request.files['image']

            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                product_data = {
                    'name': name,
                    'category': category,
                    'price': f"{price} {price_unit}",  # Store price with unit
                    'image': filename,
                    'farmer_id': ObjectId(session['user_id']),
                    'farmer_name': farmer_name,
                    'farmer_location': farmer_location
                }

                # Insert product data into products collection
                products_collection.insert_one(product_data)
                return redirect(url_for('farmer_dashboard'))

        return render_template('farmer_add_product.html', farmer_name=farmer_name, farmer_location=farmer_location)

    return redirect(url_for('farmer_login'))



# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
