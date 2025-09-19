class HRSG:
  """Service class to calculate enthalpy properties of the Heat Recovery Steam Generator"""
  def heat_supplied_calc(self, input, combustion_gas, exhaustion_temp, icph):
    """Calculation of heat supplied (in kJ/kg) to HRSG for the steam generation"""
    chimney_gas_temperature = input.chimney_gas_temperature
    combustion_gas_icph_params = combustion_gas["icph_params"]
    combustion_gas_molar_mass = combustion_gas["molar_mass"]
    combustion_gas_mass_flow = combustion_gas["mass_flow"]
    result = abs(icph.icph_calc_heat(combustion_gas_icph_params, combustion_gas_molar_mass, exhaustion_temp, chimney_gas_temperature) * combustion_gas_mass_flow)
    return result

  def get_params_operation(self, input, enthalpy_calc, entropy_calc, specific_volume_calc, saturation_parameters, high_steam_turbine, pump_inlet):
    """Calculation of params of operation of HRSG, and from others equipments of Rankine Cycle.
    Like as enthalpy of steam to be reheated and inlet water"""
    # Intern params of HRSG
    # Overheated steams generated
    high_steam_enthaply = enthalpy_calc.overheated_steam(input.high_steam_level_pressure, input.high_steam_level_temperature, saturation_parameters)
    medium_steam_enthaply = enthalpy_calc.overheated_steam(input.medium_steam_level_pressure, input.medium_steam_level_temperature, saturation_parameters)
    low_steam_enthaply = enthalpy_calc.overheated_steam(input.low_steam_level_pressure, input.low_steam_level_temperature, saturation_parameters)

    # Saturated liquid of purge
    high_purge_enthalpy = enthalpy_calc.saturated_liquid(input.high_steam_level_pressure, saturation_parameters)
    medium_purge_enthalpy = enthalpy_calc.saturated_liquid(input.medium_steam_level_pressure, saturation_parameters)
    low_purge_enthalpy = enthalpy_calc.saturated_liquid(input.low_steam_level_pressure, saturation_parameters)

    # Extern params
    medium_steam_cold_enthaply = 1
    inlet_water_enthalpy = 1

    return {
      "high_steam_enthaply": high_steam_enthaply,
      "medium_steam_enthaply": medium_steam_enthaply,
      "low_steam_enthaply": low_steam_enthaply,
      "high_purge_enthalpy": high_purge_enthalpy,
      "medium_purge_enthalpy": medium_purge_enthalpy,
      "low_purge_enthalpy": low_purge_enthalpy
    }
  
  def get_mass_flow(self):
    """Calculation of mass flows in Heat Recovery Steam Generator (Steam generated, purge, boiler feed water) in kg/h"""

    return