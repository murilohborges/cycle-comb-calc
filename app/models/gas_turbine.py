from pydantic import BaseModel

class GasTurbineInput(BaseModel):
  """
    Variables for gas turbine calculations
  """
  excess_air_percent: float
  relative_humidity: float
  gas_turbine_efficiency: float

