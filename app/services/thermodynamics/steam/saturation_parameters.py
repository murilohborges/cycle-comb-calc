import math

class SaturationParameters:
  """
  Service class to calculate saturations properties.
  """
  def saturation_temperature(self, pressure):
    """Calculation of saturation temperature(Celsius) from pressure in bar"""
    pressure = pressure/10
    A = 0
    B = 0
    C = 0
    if 0.000611 <= pressure and pressure < 12.33:
      A = 42.6776
      B = -3892.7
      C = -9.48654
    if 12.33 <= pressure and pressure <= 22.1:
      A = -387.592
      B = -12587.5
      C = -15.2578
    if pressure < 0.000611 or pressure > 22.1:
      raise ValueError(f"Pressure invalid: out of the range")
    
    Tsat = (A + (B / (math.log(pressure) + C))) - 273.15
    return Tsat

  def saturation_pressure(self, temperature):
    """Calculation of saturation pressure(bar) from temperature in celsius"""
    temperature = temperature + 273.15
    if temperature < 273.16 or temperature > 647.3:
      raise ValueError(f"Temperature invalid: out of the range")
    A0 = 10.4592
    A1 = -0.00404897
    A2 = -0.000041752
    A3 = 0.00000036851
    A4 = -0.0000000010152
    A5 = 8.6531E-13
    A6 = 9.03668E-16
    A7 = -1.9969E-18
    A8 = 7.79287E-22
    A9 = 1.91482E-25
    A10 = -3968.06
    A11 = 39.5735
    
    result = (A0 + A1 * (temperature ** 1) + A2 * (temperature ** 2) + A3 * (temperature ** 3) + A4 * (temperature ** 4) + A5 * (temperature ** 5) + A6 * (temperature ** 6) + A7 * (temperature ** 7) + A8 * (temperature ** 8) + A9 * (temperature ** 9)) + (A10 / (temperature - A11))
    Psat = math.exp(result) * 10

    return Psat
  
  def saturation_factor(self, saturation_temp, A, B, C, D, E1, E2, E3, E4, E5, E6, E7):
    """Calculation of the saturation factor (dimensionless) from the saturation temperature and other parameters. 
    According to the property to be calculated (enthalpy, entropy and others)
    """
    saturation_temp = saturation_temp + 273.15
    Tcr = 647.3
    Tc = (Tcr - saturation_temp) / Tcr
    
    result = A + B * (Tc ** (1 / 3)) + C * (Tc ** (5 / 6)) + D * (Tc ** (7 / 8)) + (E1 * (Tc ** 1) + E2 * (Tc ** 2) + E3 * (Tc ** 3) + E4 * (Tc ** 4) + E5 * (Tc ** 5) + E6 * (Tc ** 6) + E7 * (Tc ** 7))
    
    return result