from lib.models.dealership import Dealership
from lib.models.vehicle import Vehicle
from lib.models.customer import Customer
from lib.helpers import setup_database

def debug():
    session = setup_database()
    try:
        # Create a dealership
        dealership = Dealership.create(session, "Nairobi EV Hub", "Nairobi")
        print(f"Created dealership: {dealership.name}")

        # Create a customer
        customer = Customer.create(session, "John Doe", "john@example.com")
        print(f"Created customer: {customer.name}")

        # Create a vehicle
        vehicle = Vehicle.create(session, "EV Bolt", 30000, dealership.id, customer.id)
        print(f"Created vehicle: {vehicle.model}")

        # List all dealerships
        print("\nAll Dealerships:")
        for d in Dealership.get_all(session):
            print(f"ID: {d.id}, Name: {d.name}, Location: {d.location}")

        # List all vehicles for dealership
        print(f"\nVehicles for {dealership.name}:")
        for v in dealership.vehicles:
            print(f"ID: {v.id}, Model: {v.model}, Price: ${v.price}")

        # List all vehicles for customer
        print(f"\nVehicles purchased by {customer.name}:")
        for v in customer.vehicles:
            print(f"ID: {v.id}, Model: {v.model}, Price: ${v.price}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == '__main__':
    debug()