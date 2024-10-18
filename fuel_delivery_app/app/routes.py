from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Order, User, DeliveryPerson
from datetime import datetime
import random
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/place-order', methods=['GET', 'POST'])
def place_order():
    # Simulate a hardcoded customer (no login required)
    customer_id = 1  # You can hardcode a user with ID 1 for demo purposes
    customer = User.query.get(customer_id)

    if request.method == 'POST':
        try:
            address = request.form['address']
            fuel_quantity = int(request.form['fuel_quantity'])
            time_window_start = datetime.strptime(request.form['time_window_start'], '%Y-%m-%dT%H:%M')
            time_window_end = datetime.strptime(request.form['time_window_end'], '%Y-%m-%dT%H:%M')

            # Create a new order
            new_order = Order(
                address=address,
                fuel_quantity=fuel_quantity,
                time_window_start=time_window_start,
                time_window_end=time_window_end,
                customer_id=customer.id
            )

            db.session.add(new_order)
            db.session.commit()

            flash("Order placed successfully!", "success")
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error placing order: {str(e)}", "danger")

    return render_template('customer_order.html')

@bp.route('/track-order/<int:customer_id>', methods=['GET'])
def track_order(customer_id):
    orders = Order.query.filter_by(customer_id=customer_id).all()
    if not orders:
        flash("No orders found.", "warning")
    return render_template('track_order.html', orders=orders)

@bp.route('/admin', methods=['GET'])
def admin_dashboard():
    try:
        orders = Order.query.all()  # Fetch all orders
        delivery_people = DeliveryPerson.query.all()  # Fetch all delivery personnel

        # Calculate fuel details
        total_assigned_fuel = sum(order.fuel_quantity for order in orders if order.status == 'assigned')
        extra_fuel = 5000 - total_assigned_fuel  # Assuming 5000L is available at the start
        fuel_needed = sum(order.fuel_quantity for order in orders if order.status == 'pending')

        return render_template('admin_dashboard.html', orders=orders, delivery_people=delivery_people,
                               total_assigned_fuel=total_assigned_fuel, extra_fuel=extra_fuel, fuel_needed=fuel_needed)
    except Exception as e:
        flash(f"Error loading admin dashboard: {str(e)}", "danger")
        return redirect(url_for('main.index'))

@bp.route('/assign-order/<int:order_id>', methods=['POST'])
def assign_order(order_id):
    try:
        delivery_person_id = request.form['delivery_person_id']
        order = Order.query.get(order_id)
        delivery_person = DeliveryPerson.query.get(delivery_person_id)

        if not order or not delivery_person:
            flash("Error: Invalid order or delivery person.", "danger")
            return redirect(url_for('main.admin_dashboard'))

        order.assigned_to = delivery_person.id
        order.status = 'assigned'
        db.session.commit()

        flash(f"Order {order.id} assigned to {delivery_person.name}.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error assigning order: {str(e)}", "danger")

    return redirect(url_for('main.admin_dashboard'))

@bp.route('/delivery-person/<int:delivery_person_id>', methods=['GET'])
def delivery_person_view(delivery_person_id):
    # Fetch the delivery person
    delivery_person = DeliveryPerson.query.get(delivery_person_id)
    
    if not delivery_person:
        flash("Delivery person not found", "danger")
        return "Delivery person not found", 404
    
    # Fetch all assigned orders
    assigned_orders = Order.query.filter_by(assigned_to=delivery_person.id, status='assigned').all()

    if len(assigned_orders) == 0:
        flash("No orders assigned to this delivery person.", "info")
        return render_template('delivery_person_route.html', delivery_person=delivery_person, optimized_orders=[], total_time=0, total_time_completed=0, progress_percentage=0)
    
    # Generate the distance matrix
    num_locations = len(assigned_orders)
    distance_matrix = generate_distance_matrix(num_locations)

    # Optimize the route using TSP
    optimized_order_indices = tsp_optimize_route(distance_matrix)

    if optimized_order_indices is None:
        flash("No valid route found for the assigned orders.", "danger")
        return render_template('delivery_person_route.html', delivery_person=delivery_person, optimized_orders=[], total_time=0, total_time_completed=0, progress_percentage=0)

    # Get the optimized orders in sequence
    optimized_orders = [assigned_orders[i] for i in optimized_order_indices]

    # Simulate time estimation for each delivery
    delivery_times = [(order, 15 + 5 * index) for index, order in enumerate(optimized_orders)]
    total_time = sum(time for _, time in delivery_times)
    
    # Simulate that half of the orders have been completed (for demo purposes)
    completed_orders_count = len(optimized_orders) // 2
    total_time_completed = sum(time for _, time in delivery_times[:completed_orders_count])

    # Calculate progress percentage
    progress_percentage = (total_time_completed / total_time) * 100 if total_time > 0 else 0

    # Pass variables to the template
    return render_template('delivery_person_route.html', delivery_person=delivery_person,
                           optimized_orders=delivery_times, total_time=total_time, total_time_completed=total_time_completed, progress_percentage=progress_percentage)


def generate_distance_matrix(num_locations):
    # Simulate distances between locations (symmetric TSP) with 0 distance to itself
    return [[random.randint(10, 50) if i != j else 0 for j in range(num_locations)] for i in range(num_locations)]

def tsp_optimize_route(distance_matrix):
    """Solves the TSP using OR-Tools and returns the optimized order sequence."""
    num_locations = len(distance_matrix)

    # Create the routing index manager
    manager = pywrapcp.RoutingIndexManager(num_locations, 1, 0)

    # Create Routing Model
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        # Returns the distance between two locations
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc (distance between locations)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Set parameters for the search
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        # Return the optimized order sequence
        return [manager.IndexToNode(solution.Value(routing.NextVar(i))) for i in range(num_locations)]
    else:
        # If no solution, return None or handle the case
        return None
