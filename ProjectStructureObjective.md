
# Fuel Delivery Optimization System - Project Objective

## Objective
This project aims to develop a minimal Flask-based web application to handle customer fuel orders, manage deliveries, and optimize delivery routes for delivery personnel without relying on paid APIs like Google Maps. The application will mimic real-world fuel delivery operations, using open-source tools and algorithms to plan and optimize delivery routes.

### Key Features
1. **Customer Order Placement**
   - Customers can place their fuel delivery orders by providing essential details, such as location, time window, and required fuel amount.
   - A minimal user interface for customers to fill out an order form.

2. **Admin Order Management**
   - Admin users can view all pending and assigned orders in a centralized dashboard.
   - The admin can assign orders to a suitable delivery person from a list of available delivery personnel.
   - The dashboard will display order details, such as location, time window, and fuel demand.

3. **Delivery Person Route Optimization**
   - Delivery personnel can log in and view the orders assigned to them.
   - The system will generate an optimized route for the delivery person based on the assigned orders, considering time windows and vehicle capacity constraints.
   - Route optimization will be done using an open-source library like OR-Tools for Vehicle Routing Problems (VRP).

### Project Structure

```bash
fuel_delivery_app/
│
├── app/
│   ├── __init__.py          # Initializes Flask app
│   ├── models.py            # Defines database models (User, Order, DeliveryPerson, etc.)
│   ├── routes.py            # Contains API endpoints for order placement, assignment, and route optimization
│   ├── static/
│   └── templates/
│       ├── base.html        # Base HTML template
│       ├── customer_order.html  # Customer order placement form
│       ├── admin_dashboard.html # Admin dashboard for order management
│       ├── delivery_person_route.html  # Delivery person view for optimized routes
│
├── config.py                # Configuration for the application
├── requirements.txt         # Dependencies (Flask, OR-Tools, etc.)
├── run.py                   # Entry point for running the Flask app
├── projectObjective.md       # Project objective (this file)
└── README.md                # General project information and setup instructions

```

### Detailed Feature Description

#### 1. Customer Order Placement
Customers will be presented with a simple order form to place their fuel delivery requests. The form will collect:
   - Delivery Address (input field)
   - Fuel Quantity (numeric field)
   - Preferred Delivery Time Window (dropdown/select options)

**Implementation:**
- A new order entry is created in the database when a customer submits the order form.
- Data validation will ensure that orders include all necessary fields.

#### 2. Admin Order Management
Admins can view all incoming orders via an admin dashboard. Each order will have the following details:
   - Customer's delivery address
   - Time window for delivery
   - Fuel amount
   - Status of the order (Pending, Assigned, Delivered)

Admins will be able to assign orders to delivery personnel. The system will automatically check the delivery person's available capacity and make sure the assigned order can be handled.

**Implementation:**
- Orders will be displayed in a table format.
- Admins can click on an order to view details and assign it to a delivery person.
- A dropdown will allow the admin to select a delivery person.

#### 3. Delivery Person Route Optimization
Once a delivery person is assigned orders, they will be presented with an optimized route that considers:
   - Geographical proximity of orders (using K-Means for clustering locations)
   - Time window constraints for deliveries
   - Vehicle capacity for the delivery person

**Implementation:**
- OR-Tools (Open Source) will be used to generate an optimized route based on the available orders for the delivery person.
- The routes will be displayed on the delivery person's dashboard, showing a sequence of stops and estimated delivery times.
- No paid mapping services will be used; the system will simulate route optimization based on distance matrices built internally using random values or approximations.

#### Tools and Technologies
- **Flask**: For building the web application.
- **SQLite**: For database management (storing orders, users, and delivery assignments).
- **OR-Tools**: For route optimization, solving the Vehicle Routing Problem (VRP).
- **HTML/CSS/Bootstrap**: For creating the user interface.
- **Jinja2**: Flask’s templating engine to render dynamic HTML.
- **K-Means Clustering**: To group orders based on proximity before optimizing the route.

### Step-by-Step Implementation

#### Step 1: Setting Up the Flask App
1. Install Flask and necessary dependencies from `requirements.txt`.
2. Set up Flask’s app structure, with templates for the customer order form, admin dashboard, and delivery personnel dashboard.

#### Step 2: Create Database Models
Define models in `models.py` for:
- **Order**: To store order details (address, fuel quantity, time window, etc.).
- **User**: To differentiate between customers, admins, and delivery personnel.
- **DeliveryPerson**: To track delivery assignments and vehicle capacity.

#### Step 3: Customer Order Placement
1. Create a form for customers to place their orders.
2. Validate form input and store the order in the database.

#### Step 4: Admin Dashboard and Order Assignment
1. Create an admin dashboard that displays all pending orders.
2. Provide an interface for admins to assign orders to delivery personnel.

#### Step 5: Route Optimization for Delivery Personnel
1. Use K-Means to group orders based on proximity.
2. Optimize the delivery route using OR-Tools, considering time windows and capacity constraints.
3. Display the optimized route to the delivery person.

### Future Improvements
1. **Real-time Tracking**: In future iterations, real-time tracking can be implemented using WebSockets to provide updates on delivery status.
2. **Traffic Data Integration**: If needed, free traffic data sources can be integrated into the system to refine route optimization.
3. **Mobile App**: Consider adding a mobile-friendly version or a dedicated app for delivery personnel.

