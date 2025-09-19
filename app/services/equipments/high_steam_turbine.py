class HighSteamTurbine:
  """Service class to calculate properties of high pressure steam turbine"""
  def get_params_operation(self, input, saturation_parameters, entropy, enthalpy, secant_method):
    """Calculation of params of operation of High Level Steam Turbine"""
    efficiency = input.high_steam_level_efficiency

    # Inlet params
    inlet_entropy = entropy.overheated_steam(input.high_steam_level_pressure, input.high_steam_level_temperature, saturation_parameters)
    inlet_enthalpy = enthalpy.overheated_steam(input.high_steam_level_pressure, input.high_steam_level_temperature, saturation_parameters)

    # Estimating outlet enthalpy of process isentropic
    outlet_temperature_isentropic = secant_method.run(inlet_entropy, entropy, input.medium_steam_level_pressure, saturation_parameters)
    outlet_enthalpy_isentropic = enthalpy.overheated_steam(input.medium_steam_level_pressure, outlet_temperature_isentropic, saturation_parameters)

    # Estimating real outlet enthalpy 
    delta_enthalpy_isentropic = outlet_enthalpy_isentropic - inlet_enthalpy
    delta_enthalpy_real = delta_enthalpy_isentropic * (efficiency/100)
    outlet_enthalpy_real = inlet_enthalpy + delta_enthalpy_real
    
    return {
      "delta_enthalpy_real": delta_enthalpy_real,
      "outlet_enthalpy_real": outlet_enthalpy_real
      }