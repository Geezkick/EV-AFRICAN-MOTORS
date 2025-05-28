from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base, Session

class Dealership(Base):
    __tablename__ = 'dealerships'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    vehicles = relationship("Vehicle", back_populates="dealership", cascade="all, delete")

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
        except:
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