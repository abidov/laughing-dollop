from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base


def setup_database():
    """Function to initialize database, returns session"""
    engine = create_engine("sqlite:///sqlite.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
