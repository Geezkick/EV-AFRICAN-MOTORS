from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class Dealership(Base):
    __tablename__ = 'dealerships'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    vehicles = relationship("Vehicle", back_populates="dealership")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Location must be a non-empty string")
        self._location = value

    @classmethod
    def create(cls, session, name, location):
        try:
            dealership = cls(name=name, location=location)
            session.add(dealership)
            session.commit()
            return dealership
        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to create dealership: Invalid data")

    @classmethod
    def delete(cls, session, id):
        dealership = session.query(cls).get(id)
        if dealership:
            session.delete(dealership)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).get(id)

class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True)
    model = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    dealership_id = Column(Integer, ForeignKey('dealerships.id'), nullable=False)
    dealership = relationship("Dealership", back_populates="vehicles")

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Model must be a non-empty string")
        self._model = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Price must be a positive number")
        self._price = float(value)

    @classmethod
    def create(cls, session, model, price, dealership_id):
        try:
            if not session.query(Dealership).get(dealership_id):
                raise ValueError("Invalid dealership ID")
            vehicle = cls(model=model, price=price, dealership_id=dealership_id)
            session.add(vehicle)
            session.commit()
            return vehicle
        except IntegrityError:
            session.rollback()
            raise ValueError("Failed to create vehicle: Invalid data")

    @classmethod
    def delete(cls, session, id):
        vehicle = session.query(cls).get(id)
        if vehicle:
            session.delete(vehicle)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).get(id)