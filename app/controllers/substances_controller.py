from sqlmodel import Session, select
from app.database.models import Substance
from app.database.engine import engine

def get_all_substances() -> list[Substance]:
  with Session(engine) as session:
    statement = select(Substance)
    results = session.exec(statement).all()
    return results
