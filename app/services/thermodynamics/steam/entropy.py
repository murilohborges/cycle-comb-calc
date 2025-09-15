import math

class Entropy:
  """Service class to calculate entropy properties of steam"""
  def saturated_liquid(self, pressure, saturation_parameters):
    """Calculate entropy of saturated liquid in kJ/(kg*K)"""
    saturation_temperature = saturation_parameters.saturation_temperature(pressure)

    # Converting saturation temperature to Kelvin
    saturation_temperature += 273.15

    critical_point_entropy = 0
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
      critical_point_entropy = 4.4289
      A = 0
      B = 0
      C = 0
      D = 0
      E1 = -1836.92956
      E2 = 14706.6352
      E3 = -43146.6046
      E4 = 48606.6733
      E5 = 7997.5096
      E6 = -58333.9887
      E7 = 33140.0718
    if 300 <= saturation_temperature and saturation_temperature < 600:
      critical_point_entropy = 4.4289
      A = 0.912762917
      B = 0
      C = 0
      D = 0
      E1 = -1.75702956
      E2 = 1.68754095
      E3 = 5.82215341
      E4 = -63.3354786
      E5 = 188.076546
      E6 = -252.344531
      E7 = 128.058531
    if 600 <= saturation_temperature and saturation_temperature <= 647.3:
      critical_point_entropy = 4.4289
      A = 1
      B = -0.32481765
      C = -2.990556709
      D = 3.23419
      E1 = -0.678067859
      E2 = -1.91910364
      E3 = 0
      E4 = 0
      E5 = 0
      E6 = 0
      E7 = 0
    if saturation_temperature < 273.16 and saturation_temperature > 647.3:
      raise ValueError(f"Pressure invalid: out of the range")

    result = saturation_parameters.saturation_factor(saturation_temperature, A, B, C, D, E1, E2, E3, E4, E5, E6, E7) * critical_point_entropy
    return result

  def saturated_steam(self, pressure, saturation_parameters):
    """Calculate entropy of saturated steam in kJ/(kg*K)"""
    saturation_temperature = saturation_parameters.saturation_temperature(pressure)

    # Converting saturation temperature to Kelvin
    saturation_temperature += 273.15

    critical_point_entropy = 4.4289
    A = 1
    B = 0.377391
    C = -2.78368
    D = 6.93135
    E1 = -4.34839
    E2 = 1.34672
    E3 = 1.75261
    E4 = -6.22295
    E5 = 9.99004
    E6 = 0
    E7 = 0

    result = saturation_parameters.saturation_factor(saturation_temperature, A, B, C, D, E1, E2, E3, E4, E5, E6, E7) * critical_point_entropy
    return result

  def overheated_steam(self, pressure, temperature, saturation_parameters):
    """Calculate entropy of overheated steam in kJ/(kg*K)"""
    saturation_temperature = saturation_parameters.saturation_temperature(pressure)
    # Converting temperatures in Kelvin
    temperature += 273.15
    saturation_temperature += 273.15
    # Converting pressure in MegaPascal after calculating saturation_temperature
    pressure = pressure/10

    M = 85
    A0 = 4.6162961
    A1 = 0.01039008
    A2 = -0.000009873085
    A3 = 0.00000000543411
    A4 = -1.170465E-12
    B1 = -0.4650306
    B2 = 0.001
    C0 = 1.777804
    C1 = -0.01802468
    C2 = 0.00006854459
    C3 = -0.0000001184424
    C4 = 8.142201E-11

    result = (A0 + A1 * temperature + A2 * (temperature ** 2) + A3 * (temperature ** 3) + A4 * (temperature ** 4)) + (B1 * math.log(10 * pressure + B2)) - (C0 + C1 * saturation_temperature + C2 * (saturation_temperature ** 2) + C3 * (saturation_temperature ** 3) + C4 * (saturation_temperature ** 4)) * (math.exp((saturation_temperature - temperature) / M))


    return result
