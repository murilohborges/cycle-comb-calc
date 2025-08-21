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
  
  def get_all(self):
    """
      Return all substances as dict indexed by name.
      Example:
      {
        "methane": {
            "id": 1
            "molar_mass": 16.04,
            "lower_calorific_value": 802_300
          },
        "ethane": {
          "id": 2
          "molar_mass": 30.07,
          "lower_calorific_value": 1428_000
        }
      }
    """
    statement = select(
      Substance.id,
      Substance.name,
      Substance.molar_mass,
      Substance.lower_calorific_value
    )
    result = self.session.exec(statement).all()

    # Returning a dictionary indexed by name
    return {
      name: {
        "id": id_,
        "molar_mass": molar_mass,
        "lower_calorific_value": lower_calorific_value
      }
      for id_, name, molar_mass, lower_calorific_value in result
    }
  