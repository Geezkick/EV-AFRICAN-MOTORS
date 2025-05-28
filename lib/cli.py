import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import click
from lib.models.dealership import Dealership
from lib.models.vehicle import Vehicle
from lib.models.customer import Customer
from lib.helpers import setup_database

@click.group()
def cli():
    """EV African Motors CLI"""
    pass

@cli.command()
@click.option('--name', prompt='Dealership name', help='Name of the dealership')
@click.option('--location', prompt='Location', help='Location of the dealership')
def create_dealership(name, location):
    session = setup_database()
    try:
        if not name.strip():
            raise ValueError("Dealership name cannot be empty")
        if not location.strip():
            raise ValueError("Location cannot be empty")
        dealership = Dealership.create(session, name, location)
        click.echo(f"Created dealership: {dealership.name} at {dealership.location}")
    except ValueError as e:
        click.echo(f"Error: {e}")
    except Exception as e:
        click.echo(f"Unexpected error: {e}")
    finally:
        session.close()

@cli.command()
@click.option('--id', prompt='Dealership ID', type=int, help='ID of the dealership to delete')
def delete_dealership(id):
    session = setup_database()
    try:
        if Dealership.delete(session, id):
            click.echo(f"Deleted dealership with ID {id}")
        else:
            click.echo(f"Error: Dealership with ID {id} not found")
    except Exception as e:
        click.echo(f"Error deleting dealership: {e}")
    finally:
        session.close()

@cli.command()
def list_dealerships():
    session = setup_database()
    try:
        dealerships = Dealership.get_all(session)
        if not dealerships:
            click.echo("No dealerships found.")
        for d in dealerships:
            click.echo(f"ID: {d.id}, Name: {d.name}, Location: {d.location}")
    except Exception as e:
        click.echo(f"Error listing dealerships: {e}")
    finally:
        session.close()

@cli.command()
@click.option('--id', prompt='Dealership ID', type=int, help='ID of the dealership to find')
def find_dealership(id):
    session = setup_database()
    try:
        dealership = Dealership.find_by_id(session, id)
        if dealership:
            click.echo(f"ID: {dealership.id}, Name: {dealership.name}, Location: {dealership.location}")
        else:
            click.echo(f"Error: Dealership with ID {id} not found")
    except Exception as e:
        click.echo(f"Error finding dealership: {e}")
    finally:
        session.close()

@cli.command()
@click.option('--id', prompt='Dealership ID', type=int, help='ID of the dealership')
def list_dealership_vehicles(id):
    session = setup_database()
    try:
        dealership = Dealership.find_by_id(session, id)
        if dealership:
            click.echo(f"Vehicles for {dealership.name}:")
            if not dealership.vehicles:
                click.echo("  No vehicles found.")
            for vehicle in dealership.vehicles:
                click.echo(f"  ID: {vehicle.id}, Model: {vehicle.model}, Price: ${vehicle.price}")
        else:
            click.echo(f"Error: Dealership with ID {id} not found")
    except Exception as e:
        click.echo(f"Error listing vehicles: {e}")
    finally:
        session.close()

@cli.command()
@click.option('--model', prompt='Vehicle model', help='Model of the vehicle')
@click.option('--price', prompt='Price', type=float, help='Price of the vehicle')
@click.option('--dealership_id', prompt='Dealership ID', type=int, help='ID of the dealership')
@click.option('--customer_id', prompt='Customer ID (optional, press Enter to skip)', type=int, default=None, help='ID of the customer')
def create_vehicle(model, price, dealership_id, customer_id):
    session = setup_database()
    try:
        if not model.strip():
            raise ValueError("Vehicle model cannot be empty")
        if price <= 0:
            raise ValueError("Price must be a positive number")
        vehicle = Vehicle.create(session, model, price, dealership_id, customer_id)
        click.echo(f"Created vehicle: {vehicle.model}, Price: ${vehicle.price}")
    except ValueError as e:
        click.echo(f"Error: {e}")
    except Exception as e:
        click.echo(f"Unexpected error: {e}")
    finally:
        session.close()

@cli.command()
@click.option('--id', prompt='Vehicle ID', type=int, help='ID of the vehicle to delete')
def delete_vehicle(id):
    session = setup_database()
    try:
        if Vehicle.delete(session, id):
            click.echo(f"Deleted vehicle with ID {id}")
        else:
            click.echo(f"Error: Vehicle with ID {id} not found")
    except Exception as e:
        click.echo(f"Error deleting vehicle: {e}")
    finally:
        session.close()

@cli.command()
def list_vehicles():
    session = setup_database()
    try:
        click.echo("Fetching vehicles...")
        vehicles = Vehicle.get_all(session)
        if not vehicles:
            click.echo("No vehicles found.")
        for v in vehicles:
            click.echo(f"ID: {v.id}, Model: {v.model}, Price: ${v.price}, Dealership ID: {v.dealership_id}, Customer ID: {v.customer_id}")
    except Exception as e:
        click.echo(f"Error listing vehicles: {e}")
    finally:
        session.close()

@cli.command()
@click.option('--id', prompt='Vehicle ID', type=int, help='ID of the vehicle to find')
def find_vehicle(id):
    session = setup_database()
    try:
        vehicle = Vehicle.find_by_id(session, id)
        if vehicle:
            click.echo(f"ID: {vehicle.id}, Model: {vehicle.model}, Price: ${vehicle.price}, Dealership ID: {vehicle.dealership_id}, Customer ID: {v.customer_id}")
        else:
            click.echo(f"Error: Vehicle with ID {id} not found")
    except Exception as e:
        click.echo(f"Error finding vehicle: {e}")
    finally:
        session.close()

@cli.command()
@click.option('--name', prompt='Customer name', help='Name of the customer')
@click.option('--email', prompt='Email', help='Email of the customer')
def create_customer(name, email):
    session = setup_database()
    try:
        if not name.strip():
            raise ValueError("Customer name cannot be empty")
        if not email.strip() or '@' not in email:
            raise ValueError("Email must be a valid non-empty string")
        customer = Customer.create(session, name, email)
        click.echo(f"Created customer: {customer.name}, Email: {customer.email}")
    except ValueError as e:
        click.echo(f"Error: {e}")
    except Exception as e:
        click.echo(f"Unexpected error: {e}")
    finally:
        session.close()

@cli.command()
@click.option('--id', prompt='Customer ID', type=int, help='ID of the customer to delete')
def delete_customer(id):
    session = setup_database()
    try:
        if Customer.delete(session, id):
            click.echo(f"Deleted customer with ID {id}")
        else:
            click.echo(f"Error: Customer with ID {id} not found")
    except Exception as e:
        click.echo(f"Error deleting customer: {e}")
    finally:
        session.close()

@cli.command()
def list_customers():
    session = setup_database()
    try:
        customers = Customer.get_all(session)
        if not customers:
            click.echo("No customers found.")
        for c in customers:
            click.echo(f"ID: {c.id}, Name: {c.name}, Email: {c.email}")
    except Exception as e:
        click.echo(f"Error listing customers: {e}")
    finally:
        session.close()

@cli.command()
@click.option('--id', prompt='Customer ID', type=int, help='ID of the customer to find')
def find_customer(id):
    session = setup_database()
    try:
        customer = Customer.find_by_id(session, id)
        if customer:
            click.echo(f"ID: {customer.id}, Name: {customer.name}, Email: {customer.email}")
        else:
            click.echo(f"Error: Customer with ID {id} not found")
    except Exception as e:
        click.echo(f"Error finding customer: {e}")
    finally:
        session.close()

@cli.command()
@click.option('--id', prompt='Customer ID', type=int, help='ID of the customer')
def list_customer_vehicles(id):
    session = setup_database()
    try:
        customer = Customer.find_by_id(session, id)
        if customer:
            click.echo(f"Vehicles purchased by {customer.name}:")
            if not customer.vehicles:
                click.echo("  No vehicles found.")
            for vehicle in customer.vehicles:
                click.echo(f"  ID: {vehicle.id}, Model: {vehicle.model}, Price: ${vehicle.price}")
        else:
            click.echo(f"Error: Customer with ID {id} not found")
    except Exception as e:
        click.echo(f"Error listing vehicles: {e}")
    finally:
        session.close()

def main():
    while True:
        click.echo("\nEV African Motors Menu:")
        click.echo("1. Create Dealership")
        click.echo("2. Delete Dealership")
        click.echo("3. List Dealerships")
        click.echo("4. Find Dealership by ID")
        click.echo("5. List Vehicles for Dealership")
        click.echo("6. Create Vehicle")
        click.echo("7. Delete Vehicle")
        click.echo("8. List Vehicles")
        click.echo("9. Find Vehicle by ID")
        click.echo("10. Create Customer")
        click.echo("11. Delete Customer")
        click.echo("12. List Customers")
        click.echo("13. Find Customer by ID")
        click.echo("14. List Vehicles Purchased by Customer")
        click.echo("15. Exit")
        try:
            choice = click.prompt("Enter your choice (1-15)", type=int)
            click.echo(f"Selected option: {choice}")
            if choice == 1:
                create_dealership()
            elif choice == 2:
                delete_dealership()
            elif choice == 3:
                list_dealerships()
            elif choice == 4:
                find_dealership()
            elif choice == 5:
                list_dealership_vehicles()
            elif choice == 6:
                create_vehicle()
            elif choice == 7:
                delete_vehicle()
            elif choice == 8:
                list_vehicles()
            elif choice == 9:
                find_vehicle()
            elif choice == 10:
                create_customer()
            elif choice == 11:
                delete_customer()
            elif choice == 12:
                list_customers()
            elif choice == 13:
                find_customer()
            elif choice == 14:
                list_customer_vehicles()
            elif choice == 15:
                click.echo("Exiting...")
                break
            else:
                click.echo("Invalid choice. Please select 1-15.")
        except Exception as e:
            click.echo(f"Error in menu: {e}")
        click.echo("")  # Add newline for readability

if __name__ == '__main__':
    main()