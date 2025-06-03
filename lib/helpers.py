# lib/helpers.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models.base import Base
from lib.models.dealership import Dealership
from lib.models.vehicle import Vehicle
from lib.models.customer import Customer
from lib.models.payment import Payment

def setup_database():
    engine = create_engine('sqlite:///ev_african_motors.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
