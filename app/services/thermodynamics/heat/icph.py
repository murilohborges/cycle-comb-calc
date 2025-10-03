class ICPH:
  """
  Computational routine called ICPH to calculate sensible 
  heat of a flow (fuel, air or combustion gas) in kJ/kg.
  """
  def __init__(self):
        # Universal Gas Constant in J/(mol.K) 
        self.R = 8.314462618
  # Calculate heat with icph equation
  def icph_calc_heat(self, icph_params, molar_mass, temp_in, temp_out):
    A = icph_params["param_A"]
    B = icph_params["param_B"]
    C = icph_params["param_C"]
    D = icph_params["param_D"]
    temp_in = temp_in + 273.15
    temp_out = temp_out + 273.15
    tau = temp_out / temp_in

    # Validate molar mass value
    if (molar_mass <= 0):
      raise ValueError(f"Molar mass invalid: molar_mass = {molar_mass}")

    heat = (self.R/molar_mass) * ((A*temp_in*(tau - 1)) + ((B/2)*(temp_in**2)*((tau**2)-1)) + ((C/3)*(temp_in**3)*((tau**3)-1)) + ((D/temp_in)*((tau-1)/tau)))

    return heat