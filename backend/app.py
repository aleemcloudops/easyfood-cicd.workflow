from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Database initialization
def init_db():
    conn = sqlite3.connect('easyfood.db')
    cursor = conn.cursor()
    
    # Create restaurants table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            image_url TEXT,
            rating REAL DEFAULT 0,
            delivery_time TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create food_items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS food_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT,
            image_url TEXT,
            is_available BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
        )
    ''')
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            customer_address TEXT NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create order_items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            food_item_id INTEGER,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (food_item_id) REFERENCES food_items (id)
        )
    ''')
    
    # Insert sample data
    cursor.execute("SELECT COUNT(*) FROM restaurants")
    if cursor.fetchone()[0] == 0:
        # Sample restaurants
        restaurants = [
            ("Pizza Palace", "Authentic Italian pizzas with fresh ingredients", "https://via.placeholder.com/300x200", 4.5, "25-30 mins"),
            ("Burger Hub", "Juicy burgers and crispy fries", "https://via.placeholder.com/300x200", 4.2, "20-25 mins"),
            ("Spice Kitchen", "Traditional Indian cuisine with authentic spices", "https://via.placeholder.com/300x200", 4.7, "30-35 mins"),
            ("Sushi World", "Fresh sushi and Japanese delicacies", "https://via.placeholder.com/300x200", 4.6, "35-40 mins")
        ]
        
        cursor.executemany("INSERT INTO restaurants (name, description, image_url, rating, delivery_time) VALUES (?, ?, ?, ?, ?)", restaurants)
        
        # Sample food items
        food_items = [
            # Pizza Palace items
            (1, "Margherita Pizza", "Classic pizza with tomato sauce, mozzarella, and basil", 12.99, "Pizza", "https://via.placeholder.com/250x200", 1),
            (1, "Pepperoni Pizza", "Pizza topped with pepperoni and cheese", 15.99, "Pizza", "https://via.placeholder.com/250x200", 1),
            (1, "Garlic Bread", "Crispy bread with garlic and herbs", 5.99, "Sides", "https://via.placeholder.com/250x200", 1),
            
            # Burger Hub items
            (2, "Classic Burger", "Beef patty with lettuce, tomato, and cheese", 9.99, "Burgers", "https://via.placeholder.com/250x200", 1),
            (2, "Chicken Burger", "Grilled chicken with special sauce", 10.99, "Burgers", "https://via.placeholder.com/250x200", 1),
            (2, "French Fries", "Crispy golden fries", 4.99, "Sides", "https://via.placeholder.com/250x200", 1),
            
            # Spice Kitchen items
            (3, "Butter Chicken", "Creamy tomato curry with tender chicken", 14.99, "Main Course", "https://via.placeholder.com/250x200", 1),
            (3, "Biryani", "Fragrant rice with spices and meat", 16.99, "Main Course", "https://via.placeholder.com/250x200", 1),
            (3, "Naan Bread", "Soft Indian bread", 3.99, "Sides", "https://via.placeholder.com/250x200", 1),
            
            # Sushi World items
            (4, "California Roll", "Crab, avocado, and cucumber roll", 8.99, "Rolls", "https://via.placeholder.com/250x200", 1),
            (4, "Salmon Nigiri", "Fresh salmon over seasoned rice", 6.99, "Nigiri", "https://via.placeholder.com/250x200", 1),
            (4, "Miso Soup", "Traditional soybean soup", 3.99, "Soup", "https://via.placeholder.com/250x200", 1)
        ]
        
        cursor.executemany("INSERT INTO food_items (restaurant_id, name, description, price, category, image_url, is_available) VALUES (?, ?, ?, ?, ?, ?, ?)", food_items)
    
    conn.commit()
    conn.close()

# API Routes
@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    conn = sqlite3.connect('easyfood.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restaurants ORDER BY rating DESC")
    restaurants = cursor.fetchall()
    conn.close()
    
    result = []
    for restaurant in restaurants:
        result.append({
            'id': restaurant[0],
            'name': restaurant[1],
            'description': restaurant[2],
            'image_url': restaurant[3],
            'rating': restaurant[4],
            'delivery_time': restaurant[5]
        })
    
    return jsonify(result)

@app.route('/api/restaurants/<int:restaurant_id>/menu', methods=['GET'])
def get_restaurant_menu(restaurant_id):
    conn = sqlite3.connect('easyfood.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_items WHERE restaurant_id = ? AND is_available = 1", (restaurant_id,))
    items = cursor.fetchall()
    conn.close()
    
    result = []
    for item in items:
        result.append({
            'id': item[0],
            'restaurant_id': item[1],
            'name': item[2],
            'description': item[3],
            'price': item[4],
            'category': item[5],
            'image_url': item[6]
        })
    
    return jsonify(result)

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    try:
        conn = sqlite3.connect('easyfood.db')
        cursor = conn.cursor()
        
        # Create order
        cursor.execute("""
            INSERT INTO orders (customer_name, customer_phone, customer_address, total_amount, status)
            VALUES (?, ?, ?, ?, 'pending')
        """, (data['customer_name'], data['customer_phone'], data['customer_address'], data['total_amount']))
        
        order_id = cursor.lastrowid
        
        # Add order items
        for item in data['items']:
            cursor.execute("""
                INSERT INTO order_items (order_id, food_item_id, quantity, price)
                VALUES (?, ?, ?, ?)
            """, (order_id, item['food_item_id'], item['quantity'], item['price']))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'order_id': order_id, 'message': 'Order placed successfully!'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    conn = sqlite3.connect('easyfood.db')
    cursor = conn.cursor()
    
    # Get order details
    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    # Get order items
    cursor.execute("""
        SELECT oi.*, fi.name, fi.image_url 
        FROM order_items oi
        JOIN food_items fi ON oi.food_item_id = fi.id
        WHERE oi.order_id = ?
    """, (order_id,))
    items = cursor.fetchall()
    
    conn.close()
    
    order_data = {
        'id': order[0],
        'customer_name': order[1],
        'customer_phone': order[2],
        'customer_address': order[3],
        'total_amount': order[4],
        'status': order[5],
        'order_date': order[6],
        'items': []
    }
    
    for item in items:
        order_data['items'].append({
            'id': item[0],
            'food_item_id': item[2],
            'name': item[5],
            'quantity': item[3],
            'price': item[4],
            'image_url': item[6]
        })
    
    return jsonify(order_data)

@app.route('/api/search', methods=['GET'])
def search_food():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    conn = sqlite3.connect('easyfood.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT fi.*, r.name as restaurant_name
        FROM food_items fi
        JOIN restaurants r ON fi.restaurant_id = r.id
        WHERE fi.name LIKE ? OR fi.category LIKE ? OR r.name LIKE ?
        AND fi.is_available = 1
    """, (f'%{query}%', f'%{query}%', f'%{query}%'))
    
    items = cursor.fetchall()
    conn.close()
    
    result = []
    for item in items:
        result.append({
            'id': item[0],
            'restaurant_id': item[1],
            'name': item[2],
            'description': item[3],
            'price': item[4],
            'category': item[5],
            'image_url': item[6],
            'restaurant_name': item[8]
        })
    
    return jsonify(result)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)