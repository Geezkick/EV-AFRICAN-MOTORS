from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models import Base

def setup_database():
    engine = create_engine('sqlite:///lib/models/database.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()