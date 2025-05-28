from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from . import Base, Session

class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True)
    model = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    dealership_id = Column(Integer, ForeignKey('dealerships.id'), nullable=False)
    dealership = relationship("Dealership", back_populates="vehicles")
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=True)
    customer = relationship("Customer", back_populates="vehicles")

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
    def create(cls, session, model, price, dealership_id, customer_id=None):
        try:
            if not session.query(Dealership).get(dealership_id):
                raise ValueError("Invalid dealership ID")
            if customer_id and not session.query(Customer).get(customer_id):
                raise ValueError("Invalid customer ID")
            vehicle = cls(model=model, price=price, dealership_id=dealership_id, customer_id=customer_id)
            session.add(vehicle)
            session.commit()
            return vehicle
        except:
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