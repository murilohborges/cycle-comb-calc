class HRSG:
  """Service class to calculate enthalpy properties of the Heat Recovery Steam Generator"""
  def get_params_operation(self, enthalpy_calc, entropy_calc, specific_volume_calc, saturation_parameters):
    """Calculation of mass flows in Heat Recovery Steam Generator (Steam generated, purge, boiler feed water) in kg/h"""
    specific_volume = specific_volume_calc.saturated_liquid(1.01325, saturation_parameters)
    print(specific_volume)
    return