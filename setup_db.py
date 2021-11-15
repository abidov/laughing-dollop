from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base


def setup_database(db_name):
    """Function to initialize database, returns session"""
    engine = create_engine(f"sqlite:///{db_name}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
