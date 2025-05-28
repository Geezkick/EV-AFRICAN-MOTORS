import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import click
from lib.db.models import Dealership, Vehicle
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
        # Validate inputs before attempting to create
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
    if Dealership.delete(session, id):
        click.echo(f"Deleted dealership with ID {id}")
    else:
        click.echo(f"Error: Dealership with ID {id} not found")
    session.close()

@cli.command()
def list_dealerships():
    session = setup_database()
    dealerships = Dealership.get_all(session)
    for d in dealerships:
        click.echo(f"ID: {d.id}, Name: {d.name}, Location: {d.location}")
    session.close()

@cli.command()
@click.option('--id', prompt='Dealership ID', type=int, help='ID of the dealership to find')
def find_dealership(id):
    session = setup_database()
    dealership = Dealership.find_by_id(session, id)
    if dealership:
        click.echo(f"ID: {dealership.id}, Name: {dealership.name}, Location: {dealership.location}")
    else:
        click.echo(f"Error: Dealership with ID {id} not found")
    session.close()

@cli.command()
@click.option('--id', prompt='Dealership ID', type=int, help='ID of the dealership')
def list_dealership_vehicles(id):
    session = setup_database()
    dealership = Dealership.find_by_id(session, id)
    if dealership:
        click.echo(f"Vehicles for {dealership.name}:")
        for vehicle in dealership.vehicles:
            click.echo(f"  ID: {vehicle.id}, Model: {vehicle.model}, Price: ${vehicle.price}")
    else:
        click.echo(f"Error: Dealership with ID {id} not found")
    session.close()

@cli.command()
@click.option('--model', prompt='Vehicle model', help='Model of the vehicle')
@click.option('--price', prompt='Price', type=float, help='Price of the vehicle')
@click.option('--dealership_id', prompt='Dealership ID', type=int, help='ID of the dealership')
def create_vehicle(model, price, dealership_id):
    session = setup_database()
    try:
        # Validate inputs before attempting to create
        if not model.strip():
            raise ValueError("Vehicle model cannot be empty")
        if price <= 0:
            raise ValueError("Price must be a positive number")
        vehicle = Vehicle.create(session, model, price, dealership_id)
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
    if Vehicle.delete(session, id):
        click.echo(f"Deleted vehicle with ID {id}")
    else:
        click.echo(f"Error: Vehicle with ID {id} not found")
    session.close()

@cli.command()
def list_vehicles():
    session = setup_database()
    vehicles = Vehicle.get_all(session)
    for v in vehicles:
        click.echo(f"ID: {v.id}, Model: {v.model}, Price: ${v.price}, Dealership ID: {v.dealership_id}")
    session.close()

@cli.command()
@click.option('--id', prompt='Vehicle ID', type=int, help='ID of the vehicle to find')
def find_vehicle(id):
    session = setup_database()
    vehicle = Vehicle.find_by_id(session, id)
    if vehicle:
        click.echo(f"ID: {vehicle.id}, Model: {vehicle.model}, Price: ${vehicle.price}, Dealership ID: {vehicle.dealership_id}")
    else:
        click.echo(f"Error: Vehicle with ID {id} not found")
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
        click.echo("10. Exit")
        choice = click.prompt("Enter your choice (1-10)", type=int)
        
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
            click.echo("Exiting...")
            break
        else:
            click.echo("Invalid choice. Please select 1-10.")

if __name__ == '__main__':
    main()