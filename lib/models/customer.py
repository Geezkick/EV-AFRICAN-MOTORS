from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base, Session

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    vehicles = relationship("Vehicle", back_populates="customer")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or '@' not in value or not value.strip():
            raise ValueError("Email must be a valid non-empty string")
        self._email = value

    @classmethod
    def create(cls, session, name, email):
        try:
            customer = cls(name=name, email=email)
            session.add(customer)
            session.commit()
            return customer
        except:
            session.rollback()
            raise ValueError("Failed to create customer: Invalid data")

    @classmethod
    def delete(cls, session, id):
        customer = session.query(cls).get(id)
        if customer:
            session.delete(customer)
            session.commit()
            return True
        return False

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).get(id)