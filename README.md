# 🌾 AgriLink: Agricultural Marketplace Platform 🚜

## 🌟 Overview
AgriLink is a web-based platform that connects farmers directly with customers, providing a seamless marketplace for agricultural products and innovative bidding features.

## 🔑 Key Features

### 👥 User Types
- **Farmers** 👨‍🌾: Can list products, create bids, manage orders
- **Customers** 🛒: Browse products, place orders, participate in auctions

### 🌈 Main Functionalities
- 🔐 User Authentication (Signup/Login)
- 📦 Product Listing
- 🤝 Product Bidding
- 📋 Order Management
- 👤 Profile Management

## 💻 Tech Stack
- **Backend**: Flask (Python) 🐍
- **Database**: MongoDB 📊
- **Authentication**: Session-based 🔒
- **Deployment**: Ready for cloud platforms ☁️

## 🚀 Setup and Installation

### 📋 Prerequisites
- Python 3.8+ 🐍
- MongoDB 📦
- pip (Python package manager) 📥

### 🛠 Installation Steps
1. Clone the repository
```bash
git clone https://github.com/yourusername/agrilink.git
cd agrilink
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set Environment Variables
Create a `.env` file with:
```
SECRET_KEY=your_secret_key
MONGODB_URI=your_mongodb_connection_string
```

5. Run the Application
```bash
python app.py
```

## 💾 Database Collections
- `farmers` 👨‍🌾: Stores farmer account information
- `customers` 🧑‍🤝‍🧑: Stores customer account information
- `products` 🥕: Lists agricultural products
- `orders` 📦: Tracks customer orders
- `biddings` 💰: Manages product auction bids
- `bid_notifications` 🔔: Schedules future bid events

## 🗺 Core Routes
- `/` 🏠: Landing page
- `/farmer/signup` 👨‍🌾: Farmer registration
- `/customer/signup` 🛒: Customer registration
- `/farmer/dashboard` 📋: Farmer's product and bid management
- `/customer/dashboard` 🛍️: Product browsing
- `/cart/add` 🛒: Add products to cart
- `/farmer/add_bid` 💲: Create a new product bid

## 🛡️ Security Considerations
- Session-based authentication 🔐
- Password storage (recommend implementing password hashing) 🔒
- Input validation ✅
- Secure file handling 🛡️

## 🚧 Future Enhancements
- Implement password hashing 🔐
- Add more robust error handling ⚠️
- Integrate payment gateway 💳
- Implement advanced search and filtering 🔍
- Create seller/buyer ratings system ⭐

## 🤝 Contributing
1. Fork the repository 🍴
2. Create your feature branch (`git checkout -b feature/AmazingFeature`) 🌿
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`) 💾
4. Push to the branch (`git push origin feature/AmazingFeature`) 📤
5. Open a Pull Request 🚪


## 📞 Contact
Vedant Kale - vedant.kale22@pccoepune.org 📧

Project Link: [https://github.com/VedantKale106/Agrilink](https://github.com/VedantKale106/Agrilink.git) 🔗
