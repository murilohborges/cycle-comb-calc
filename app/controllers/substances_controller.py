from sqlmodel import select
from app.database.models import Substance

def get_all_substances(db) -> list[Substance]:
  statement = select(Substance)
  return db.exec(statement).all()
