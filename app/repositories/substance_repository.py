from typing import List, Tuple
from sqlmodel import select, Session
from ..database.models import Substance

class SubstanceRepository:
  """
  Repository to access data of Substance entity.
  It isolate database's access of logic from business logic.
  """

  def __init__(self, session: Session):
    self.session = session
  
  def get_all(self) -> List[Tuple[float, float]]:
    """
    Return all substances as list of tuples:
    (lower_calorific_value, molar_mass)
    """
    statement = select(Substance.lower_calorific_value, Substance.molar_mass)
    result = self.session.exec(statement).all()
    return result
  