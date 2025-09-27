# EasyFood - Food Ordering App

A complete food ordering application like Swiggy/Zomato with Flask backend and vanilla JavaScript frontend.

## Features

- 🏪 Restaurant browsing with ratings and delivery times
- 🍕 Menu viewing by restaurant with categories
- 🔍 Search functionality for food items and restaurants
- 🛒 Shopping cart with quantity management
- 📱 Responsive design for mobile and desktop
- ✅ Order placement with customer details
- 🎨 Modern, animated UI with glassmorphism effects

## Technology Stack

### Backend (Flask)
- **Flask**: Web framework
- **SQLite**: Database for storing restaurants, menu items, and orders
- **Flask-CORS**: For handling cross-origin requests

### Frontend (Vanilla JavaScript)
- **HTML5**: Structure
- **CSS3**: Styling with animations and responsive design
- **JavaScript**: Frontend logic and API integration

## Project Structure

```
easyfood/
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   └── easyfood.db        # SQLite database (auto-created)
├── frontend/
│   ├── index.html         # Main frontend file
│   └── package.json       # Frontend configuration
└── README.md              # This file
```

## Setup Instructions

### Backend Setup

1. **Create project directory and navigate to it:**
   ```bash
   mkdir easyfood
   cd easyfood
   mkdir backend frontend
   ```

2. **Set up Python virtual environment:**
   ```bash
   cd backend
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install Flask==2.3.3 Flask-CORS==4.0.0
   ```

4. **Create and run the Flask app:**
   - Save the Flask code as `app.py` in the backend folder
   - Run the application:
   ```bash
   python app.py
   ```
   
   The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd ../frontend
   ```

2. **Save the HTML file:**
   - Save the frontend code as `index.html` in the frontend folder

3. **Start a simple HTTP server:**
   ```bash
   # Using Python 3
   python -m http.server 3000
   
   # Using Node.js (if you have it installed)
   npx http-server -p 3000
   ```
   
   The frontend will be available at `http://localhost:3000`

## API Endpoints

### Restaurants
- `GET /api/restaurants` - Get all restaurants
- `GET /api/restaurants/{id}/menu` - Get menu for a specific restaurant

### Orders
- `POST /api/orders` - Create a new order
- `GET /api/orders/{id}` - Get order details

### Search
- `GET /api/search?q={query}` - Search for food items

## Database Schema

### Tables
- **restaurants**: id, name, description, image_url, rating, delivery_time
- **food_items**: id, restaurant_id, name, description, price, category, image_url, is_available
- **orders**: id, customer_name, customer_phone, customer_address, total_amount, status, order_date
- **order_items**: id, order_id, food_item_id, quantity, price

## Usage

1. **Browse Restaurants**: View all available restaurants with ratings and delivery times
2. **View Menu**: Click on any restaurant to see their menu items organized by category
3. **Search**: Use the search bar to find specific food items or restaurants
4. **Add to Cart**: Add items to your cart and manage quantities
5. **Place Order**: Fill in delivery details and place your order

## Sample Data

The application comes pre-loaded with sample data including:
- 4 restaurants (Pizza Palace, Burger Hub, Spice Kitchen, Sushi World)
- 12+ food items across different categories
- Proper categorization and pricing

## Customization

### Adding New Restaurants
```python
cursor.execute("INSERT INTO restaurants (name, description, image_url, rating, delivery_time) VALUES (?, ?, ?, ?, ?)", 
               (name, description, image_url, rating, delivery_time))
```

### Adding New Menu Items
```python
cursor.execute("INSERT INTO food_items (restaurant_id, name, description, price, category, image_url, is_available) VALUES (?, ?, ?, ?, ?, ?, ?)",
               (restaurant_id, name, description, price, category, image_url, is_available))
```

### Styling Customization
The CSS uses CSS custom properties and can be easily customized by modifying the color variables and animations in the style section.

## Production Deployment

### Backend
- Use a production WSGI server like Gunicorn
- Set up a proper database (PostgreSQL/MySQL) instead of SQLite
- Add environment variables for configuration
- Implement proper error handling and logging

### Frontend
- Serve static files through a web server like Nginx
- Optimize images and add lazy loading
- Implement service workers for offline functionality
- Add analytics and monitoring

## Future Enhancements

- User authentication and profiles
- Order tracking and status updates
- Payment gateway integration
- Restaurant owner dashboard
- Push notifications
- Reviews and ratings system
- Favorite restaurants and items
- Order history
- Delivery tracking

## License

MIT License - feel free to use this project for learning and commercial purposes.

## Support

If you encounter any issues or have questions, please check the code comments or create an issue in the repository.