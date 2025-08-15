from ..chemistry.gas_fuel import GasFuel

class GasTurbine:
  def __init__(self, input, db):
    self.input = input
    self.db = db
    self.gas_fuel = GasFuel(input, db)

  # Calculation of Heat Rate from Gas Turbine
  def heat_rate_calc(self):
    heat_rate = 3600/(self.input.gas_turbine_efficiency/100)
    return heat_rate
  