from pydantic import BaseModel

class CycleInput(BaseModel):
  '''
    All base-variables for the Cycle Combined calculation.
  '''

  temperature: float
  pressure: float
  mass_flow: float
  
