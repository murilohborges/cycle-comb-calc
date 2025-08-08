from sqlmodel import Session
from .engine import engine

def get_session():
    """
    Creating session to load the database
    """
    with Session(engine) as session:
        yield session  
