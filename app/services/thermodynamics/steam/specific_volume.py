import math
from app.services.thermodynamics.steam.saturation_parameters import SaturationParameters

class SpecificVolume:
  """Service class to calculate specific volume property of steam"""
  def __init__(self, saturation_params=None):
    self.saturation_params = saturation_params or SaturationParameters()

  def saturated_liquid(self, pressure, ):
    """Calculate specific volume of saturated liquid in m³/kg"""
    saturation_temperature = self.saturation_params.saturation_temperature(pressure)

    # Converting saturation temperature to Kelvin
    saturation_temperature += 273.15

    critical_point_specific_volume = 0.003155
    A = 1
    B = -1.9153882
    C = 12.015186
    D = -7.8464025
    E1 = -3.888614
    E2 = 2.0582238
    E3 = -2.0829991
    E4 = 0.82180004
    E5 = 0.47549742
    E6 = 0
    E7 = 0

    if saturation_temperature < 273.16 or saturation_temperature > 647.3:
      raise ValueError(f"Pressure invalid: out of the range")


    result = self.saturation_params.saturation_factor(saturation_temperature, A, B, C, D, E1, E2, E3, E4, E5, E6, E7) * critical_point_specific_volume
    return result
