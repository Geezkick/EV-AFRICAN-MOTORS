from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# lib/models/__init__.py
from .dealership import Dealership
from .vehicle import Vehicle
from .customer import Customer
from .payment import Payment

Base = declarative_base()
engine = create_engine('sqlite:///lib/models/database.db')
Session = sessionmaker(bind=engine)