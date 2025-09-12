class Enthalpy:
  """Service class to calculate enthalpy properties of steam"""
  def saturated_liquid(self, pressure, saturation_parameters):
    """Calculate enthalpy of saturated liquid in kJ/kg"""
    Ts = saturation_parameters.saturation_temperature(pressure)
    
    Hfcr = 0
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
    
    if 273.16 <= Ts and Ts < 300:
      Hfcr = 2099.3
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
    if 300 <= Ts and Ts < 600:
      Hfcr = 2099.3
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
    if 600 <= Ts and Ts <= 647.3:
      Hfcr = 2099.3
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
    if Ts < 273.16 and Ts > 647.3:
      raise ValueError(f"Pressure invalid: out of the range")
    
    Hliqsat = saturation_parameters.saturation_factor(Ts, A, B, C, D, E1, E2, E3, E4, E5, E6, E7) * Hfcr
    return Hliqsat