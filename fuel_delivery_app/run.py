import os
from app import create_app, db
from app.models import User, DeliveryPerson
import logging

# Get the FLASK_ENV environment variable to load the correct config, default to 'development'
config_name = os.getenv('FLASK_ENV', 'default')
app = create_app(config_name)

def initialize_database():
    """Initialize the database with some test data."""
    with app.app_context():
        # Ensure tables are created before querying
        db.create_all()  # This ensures that the tables (e.g., User, DeliveryPerson) are created

        # Add a test customer if not already present
        customer = User.query.filter_by(email='customer@example.com').first()
        if not customer:
            customer = User(username='test_customer', email='customer@example.com', role='customer')
            db.session.add(customer)

        # Add delivery personnel if not already present
        delivery_person1 = DeliveryPerson.query.filter_by(name='John Doe').first()
        delivery_person2 = DeliveryPerson.query.filter_by(name='Jane Smith').first()

        if not delivery_person1:
            delivery_person1 = DeliveryPerson(name='John Doe', vehicle_capacity=300)
            db.session.add(delivery_person1)

        if not delivery_person2:
            delivery_person2 = DeliveryPerson(name='Jane Smith', vehicle_capacity=250)
            db.session.add(delivery_person2)

        # Commit the changes after adding both customer and delivery personnel
        db.session.commit()

# Initialize the database with test data (if necessary)
initialize_database()

# Logging setup (for production and debugging purposes)
if config_name == 'production':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('werkzeug')
    handler = logging.FileHandler('app.log')  # Save logs to a file
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=(config_name == 'development'))
