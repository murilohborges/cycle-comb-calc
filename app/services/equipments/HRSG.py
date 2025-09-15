class HRSG:
  """Service class to calculate enthalpy properties of the Heat Recovery Steam Generator"""
  def get_params_operation(self, enthalpy_calc, entropy_calc, saturation_parameters):
    """Calculation of mass flows in Heat Recovery Steam Generator (Steam generated, purge, boiler feed water) in kg/h"""
    entropy = entropy_calc.overheated_steam(4, 400, saturation_parameters)
    print(entropy)
    return