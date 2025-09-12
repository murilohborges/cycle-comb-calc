class HRSG:
  """Service class to calculate enthalpy properties of the Heat Recovery Steam Generator"""
  def get_params_operation(self, enthalpy_calc, saturation_parameters):
    """Calculation of mass flows in Heat Recovery Steam Generator (Steam generated, purge, boiler feed water) in kg/h"""
    enthalpy = enthalpy_calc.saturated_liquid(2, saturation_parameters)
    print(enthalpy)
    return