from pydantic import BaseModel

class Substance(BaseModel):
  """
  All substances available to the simulation
  """
  name: str
  formula: str
  cas_number: str

  class ConfigDict:
    from_attributes = True
