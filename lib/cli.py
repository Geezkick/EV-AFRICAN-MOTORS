# lib/cli.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import click
from lib.models.dealership import Dealership
from lib.models.vehicle import Vehicle
from lib.models.customer import Customer
from lib.models.payment import Payment
from lib.helpers import setup_database
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from datetime import datetime

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
        dealership = Dealership.create(session, name, location)
        click.echo(f"Created dealership: {dealership.name} at {dealership.location} (ID: {dealership.id})")
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
@click.option('--dealership', prompt='Dealership name or ID', help='Name or ID of the dealership')
@click.option('--customer_id', prompt='Customer ID (optional, press Enter to skip)', type=int, default=None, help='ID of the customer', show_default=False, required=False)
def create_vehicle(model, price, dealership, customer_id):
    session = setup_database()
    try:
        try:
            dealership_id = int(dealership)
            dealership_obj = Dealership.find_by_id(session, dealership_id)
            if not dealership_obj:
                raise ValueError(f"Dealership with ID {dealership_id} not found")
        except ValueError:
            dealership_obj = session.query(Dealership).filter(func.lower(Dealership.name) == func.lower(dealership)).first()
            if not dealership_obj:
                raise ValueError(f"Dealership with name '{dealership}' not found")
            dealership_id = dealership_obj.id
        
        vehicle = Vehicle.create(session, model, price, dealership_id, customer_id)
        click.echo(f"Created vehicle: {vehicle.model}, Price: ${vehicle.price}, Dealership: {dealership_obj.name}")
        if customer_id:
            customer = Customer.find_by_id(session, customer_id)
            click.echo(f"Associated with Customer: {customer.name} (ID: {customer_id})")
    except ValueError as e:
        click.echo(f"Error: {e}")
    except IntegrityError:
        click.echo(f"Error: Failed to create vehicle due to database constraint")
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
        vehicles = Vehicle.get_all(session)
        if not vehicles:
            click.echo("No vehicles found.")
        for v in vehicles:
            dealership = Dealership.find_by_id(session, v.dealership_id)
            customer = Customer.find_by_id(session, v.customer_id) if v.customer_id else None
            click.echo(f"ID: {v.id}, Model: {v.model}, Price: ${v.price}, Dealership: {dealership.name if dealership else 'Unknown'}, Customer: {customer.name if customer else 'None'} (ID: {v.customer_id})")
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
            dealership = Dealership.find_by_id(session, vehicle.dealership_id)
            customer = Customer.find_by_id(session, vehicle.customer_id) if vehicle.customer_id else None
            click.echo(f"ID: {vehicle.id}, Model: {vehicle.model}, Price: ${vehicle.price}, Dealership: {dealership.name if dealership else 'Unknown'}, Customer: {customer.name if customer else 'None'} (ID: {vehicle.customer_id})")
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
        customer = Customer.create(session, name, email)
        click.echo(f"Created customer: {customer.name}, Email: {customer.email}, ID: {customer.id}")
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

@cli.command()
@click.option('--vehicle_id', prompt='Vehicle ID', type=int, help='ID of the vehicle')
@click.option('--customer_id', prompt='Customer ID', type=int, help='ID of the customer')
@click.option('--amount', prompt='Payment amount', type=float, help='Amount of the payment')
def create_payment(vehicle_id, customer_id, amount):
    session = setup_database()
    try:
        vehicle = Vehicle.find_by_id(session, vehicle_id)
        if not vehicle:
            raise ValueError(f"Vehicle with ID {vehicle_id} not found")
        payment = vehicle.add_payment(session, amount, customer_id)
        click.echo(f"Created payment: Amount: ${payment.amount}, Vehicle ID: {payment.vehicle_id}, Customer ID: {payment.customer_id}, Date: {payment.payment_date}")
    except ValueError as e:
        click.echo(f"Error: {e}")
    except Exception as e:
        click.echo(f"Unexpected error: {e}")
    finally:
        session.close()

@cli.command()
@click.option('--vehicle_id', prompt='Vehicle ID', type=int, help='ID of the vehicle')
def list_vehicle_payments(vehicle_id):
    session = setup_database()
    try:
        vehicle = Vehicle.find_by_id(session, vehicle_id)
        if not vehicle:
            raise ValueError(f"Vehicle with ID {vehicle_id} not found")
        payments = vehicle.get_payments(session)
        total_paid = vehicle.get_total_payments(session)
        balance = vehicle.get_remaining_balance(session)
        click.echo(f"Payments for Vehicle ID {vehicle_id} (Model: {vehicle.model}):")
        if not payments:
            click.echo("  No payments found.")
        for payment in payments:
            click.echo(f"  Payment ID: {payment.id}, Amount: ${payment.amount}, Customer ID: {payment.customer_id}, Date: {payment.payment_date}, Status: {payment.status}")
        click.echo(f"Total Paid: ${total_paid:.2f}, Remaining Balance: ${balance:.2f}")
    except ValueError as e:
        click.echo(f"Error: {e}")
    except Exception as e:
        click.echo(f"Error listing payments: {e}")
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
        click.echo("15. Create Payment")
        click.echo("16. List Payments for Vehicle")
        click.echo("17. Exit")
        try:
            choice = click.prompt("Enter your choice (1-17)", type=int)
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
                create_payment()
            elif choice == 16:
                list_vehicle_payments()
            elif choice == 17:
                click.echo("Exiting...")
                break
            else:
                click.echo("Invalid choice. Please select 1-17.")
        except ValueError:
            click.echo("Error: Please enter a valid number between 1 and 17")
        except Exception as e:
            click.echo(f"Error in menu: {e}")
        click.echo("")

if __name__ == '__main__':
    main()
