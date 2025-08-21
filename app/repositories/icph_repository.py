from typing import List, Tuple
from sqlmodel import select, Session
from ..database.models import CorrelationSpecificHeat

class ICPHRepository:
  """
  Repository to access data of CorrelationSpecificHeat entity.
  It isolate database's access of logic from business logic.
  """

  def __init__(self, session: Session):
    self.session = session
  
  def get_by_substance_id(self, substance_id_input):
    """
      Return all icph params of substances by substance_id.
      Example:
        {
          "param_A": 16.04,
          "param_B": 16.04,
          "param_C": 16.04,
          "param_D": 16.04,
        }
    """
    statement = select(
      CorrelationSpecificHeat.param_A,
      CorrelationSpecificHeat.param_B,
      CorrelationSpecificHeat.param_C,
      CorrelationSpecificHeat.param_D,
    ).where(CorrelationSpecificHeat.substance_id == substance_id_input)

    result = self.session.exec(statement).first()

    if not result:
        return None

    param_A, param_B, param_C, param_D = result
    return {
        "param_A": param_A,
        "param_B": param_B,
        "param_C": param_C,
        "param_D": param_D,
    }