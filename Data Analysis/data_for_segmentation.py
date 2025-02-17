import json
import pandas as pd
import random
from bson import ObjectId  # Simulating MongoDB ObjectId

# Sample product categories and names
products = [
    {"name": "Jwari", "category": "Grains", "price": "50 per kg"},
    {"name": "Wheat", "category": "Grains", "price": "45 per kg"},
    {"name": "Rice", "category": "Grains", "price": "60 per kg"},
    {"name": "Tomato", "category": "Vegetables", "price": "30 per kg"},
    {"name": "Onion", "category": "Vegetables", "price": "25 per kg"},
    {"name": "Apple", "category": "Fruits", "price": "100 per kg"},
    {"name": "Banana", "category": "Fruits", "price": "40 per kg"},
    {"name": "Mango", "category": "Fruits", "price": "80 per kg"},
    {"name": "Milk", "category": "Dairy", "price": "50 per liter"},
    {"name": "Yogurt", "category": "Dairy", "price": "60 per kg"},
    {"name": "Cheese", "category": "Dairy", "price": "400 per kg"},
    {"name": "Spinach", "category": "Vegetables", "price": "20 per kg"},
    {"name": "Carrot", "category": "Vegetables", "price": "35 per kg"},
    {"name": "Potato", "category": "Vegetables", "price": "20 per kg"},
    {"name": "Orange", "category": "Fruits", "price": "60 per kg"},
    {"name": "Grapes", "category": "Fruits", "price": "70 per kg"},
    {"name": "Watermelon", "category": "Fruits", "price": "30 per kg"},
    {"name": "Butter", "category": "Dairy", "price": "250 per kg"},
    {"name": "Paneer", "category": "Dairy", "price": "300 per kg"},
    {"name": "Oats", "category": "Grains", "price": "60 per kg"},
    {"name": "Barley", "category": "Grains", "price": "55 per kg"},
    {"name": "Corn", "category": "Grains", "price": "40 per kg"},
    {"name": "Lentils", "category": "Pulses", "price": "80 per kg"},  # Added Pulses category
    {"name": "Chickpeas", "category": "Pulses", "price": "70 per kg"}, # Added Pulses category
    {"name": "Kidney Beans", "category": "Pulses", "price": "90 per kg"}, # Added Pulses category
    {"name": "Sugar", "category": "Sweeteners", "price": "40 per kg"}, # Added Sweeteners category
    {"name": "Honey", "category": "Sweeteners", "price": "200 per kg"},# Added Sweeteners category
    {"name": "Jaggery", "category": "Sweeteners", "price": "60 per kg"},# Added Sweeteners category
    {"name": "Salt", "category": "Spices", "price": "20 per kg"}, # Added Spices category
    {"name": "Turmeric", "category": "Spices", "price": "150 per kg"},# Added Spices category
    {"name": "Chili Powder", "category": "Spices", "price": "100 per kg"},# Added Spices category

]

# Generate dummy customer order data
data = []
for _ in range(100):  # Generate data for 100 orders
    product = random.choice(products)
    order = {
        "_id": {"$oid": str(ObjectId())},
        "customer_id": {"$oid": str(ObjectId())},
        "product_id": {"$oid": str(ObjectId())},
        "farmer_id": {"$oid": str(ObjectId())},
        "product_name": product["name"],
        "category": product["category"],
        "quantity": random.randint(1, 10),
        "price": product["price"],
        "unit": "kg",
        "image": "https://th.bing.com/th/id/OIP.gUK1S2m2uQAXZaoplyTpagHaEo?w=277&h=180&c=7&r=0&o=5&pid=1.7",
        "status": random.choice(["Pending", "Shipped", "Delivered"]),
    }
    data.append(order)

# Save as JSON file
json_filename = "customer_orders.json"
with open(json_filename, "w") as json_file:
    json.dump(data, json_file, indent=4)

print(f"JSON data saved to {json_filename}")

# Convert JSON to CSV
df = pd.json_normalize(data)  # Flatten nested JSON for CSV format
csv_filename = "customer_orders.csv"
df.to_csv(csv_filename, index=False)

print(f"CSV file saved to {csv_filename}")
