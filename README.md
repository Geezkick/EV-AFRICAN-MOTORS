EV African Motors
EV African Motors is a Python CLI application for managing electric vehicles and dealerships in a fictional electric vehicle company. It uses SQLite for data storage and SQLAlchemy for ORM, with a command-line interface powered by Click.
Features

Manage Dealerships (create, delete, list, find by ID, view associated vehicles).
Manage Vehicles (create, delete, list, find by ID).
One-to-many relationship: One dealership can have multiple vehicles.
Input validation and error handling for user interactions.

Setup

Clone the repository:git clone https://github.com/yourusername/ev_african_motors.git
cd ev_african_motors


Install dependencies using Pipenv:pipenv install


Activate the virtual environment:pipenv shell


Run the CLI:python lib/cli/cli.py



Usage
Run the CLI with:
python lib/cli/cli.py

Follow the menu prompts to:

Create, delete, list, or find dealerships and vehicles.
View vehicles associated with a dealership.
Exit the application.

Project Structure

lib/db/models.py: Defines ORM models (Dealership, Vehicle).
lib/cli/cli.py: Implements the CLI using Click.
lib/helpers.py: Contains database setup and helper functions.
lib/db/database.db: SQLite database file.

Requirements

Python 3.9+
Pipenv
Dependencies: click, sqlalchemy

License
MIT License
