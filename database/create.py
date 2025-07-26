from sqlmodel import SQLModel
from .engine import engine
from .models import Substance, CorrelationSpecificHeat

def create_db_and_tables():
  SQLModel.metadata.create_all(engine)
