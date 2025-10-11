import math
from app.services.thermodynamics.steam.saturation_parameters import SaturationParameters

class Enthalpy:
  """Service class to calculate enthalpy properties of steam"""
  def __init__(self, saturation_params=None):
    self.saturation_params = saturation_params or SaturationParameters()

  def saturated_liquid(self, pressure):
    """Calculate enthalpy of saturated liquid in kJ/kg"""
    saturation_temperature = self.saturation_params.saturation_temperature(pressure)

    # Converting saturation temperature to Kelvin
    saturation_temperature += 273.15

    critical_point_enthalpy = 0
    A = 0
    B = 0
    C = 0
    D = 0
    E1 = 0
    E2 = 0
    E3 = 0
    E4 = 0
    E5 = 0
    E6 = 0
    E7 = 0

    if 273.16 <= saturation_temperature and saturation_temperature < 300:
      critical_point_enthalpy = 2099.3
      A = 0
      B = 0
      C = 0
      D = 0
      E1 = 624.698837
      E2 = -2343.85369
      E3 = -9508.12101
      E4 = 71628.7928
      E5 = -163535.221
      E6 = 166531.093
      E7 = -64785.4585
    if 300 <= saturation_temperature and saturation_temperature < 600:
      critical_point_enthalpy = 2099.3
      A = 0.8839230108
      B = 0
      C = 0
      D = 0
      E1 = -2.67172935
      E2 = 6.22640035
      E3 = -13.1789573
      E4 = -1.91322436
      E5 = 68.7937653
      E6 = -124.819906
      E7 = 72.1435404
    if 600 <= saturation_temperature and saturation_temperature <= 647.3:
      critical_point_enthalpy = 2099.3
      A = 1
      B = -0.441057805
      C = -5.52255517
      D = 6.43994847
      E1 = -1.164578795
      E2 = -1.30574143
      E3 = 0
      E4 = 0
      E5 = 0
      E6 = 0
      E7 = 0
    if saturation_temperature < 273.16 or saturation_temperature > 647.3:
      raise ValueError(f"Pressure invalid: out of the range")

    result = self.saturation_params.saturation_factor(saturation_temperature, A, B, C, D, E1, E2, E3, E4, E5, E6, E7) * critical_point_enthalpy
    return result

  def saturated_steam(self, pressure):
    """Calculate enthalpy of saturated steam in kJ/kg"""
    saturation_temperature = self.saturation_params.saturation_temperature(pressure)

    # Converting saturation temperature to Kelvin
    saturation_temperature += 273.15

    critical_point_enthalpy = 2099.3
    A = 1
    B = 0.457874342
    C = 5.08441288
    D = -1.48513244
    E1 = -4.81351884
    E2 = 2.69411792
    E3 = -7.39064542
    E4 = 10.4961689
    E5 = -5.46840036
    E6 = 0
    E7 = 0

    result = self.saturation_params.saturation_factor(saturation_temperature, A, B, C, D, E1, E2, E3, E4, E5, E6, E7) * critical_point_enthalpy
    return result

  def overheated_steam(self, pressure, temperature):
    """Calculate enthalpy of overheated steam in kJ/kg"""
    saturation_temperature = self.saturation_params.saturation_temperature(pressure)
    # Converting temperatures in Kelvin
    temperature += 273.15
    saturation_temperature += 273.15
    # Converting pressure in MegaPascal after calculating saturation_temperature
    pressure = pressure/10

    M = 45
    B11 = 2041.21
    B12 = -40.40021
    B13 = -0.48095
    B21 = 1.610693
    B22 = 0.05472051
    B23 = 0.0007517537
    B31 = 0.0003383117
    B32 = -0.00001975736
    B33 = -0.000000287409
    B41 = 1707.82
    B42 = -16.99419
    B43 = 0.062746295
    B44 = -0.00010284259
    B45 = 0.000000064561298

    A0 = B11 + B12 * pressure + B13 * (pressure ** 2)
    A1 = B21 + B22 * pressure + B23 * (pressure ** 2)
    A2 = B31 + B32 * pressure + B33 * (pressure ** 2)
    A3 = B41 + B42 * saturation_temperature + B43 * (saturation_temperature ** 2) + B44 * (saturation_temperature ** 3) + B45 * (saturation_temperature ** 4)

    result = (A0 + A1 * temperature + A2 * (temperature ** 2)) - (A3 * math.exp((saturation_temperature - temperature) / M))

    return result
