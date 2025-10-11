class LowSteamTurbine:
  """Service class to calculate properties of low pressure steam turbine"""
  def mixing_point_outlet_enthalpy(self, low_steam_enthalpy, medium_steam_turbine, hrsg_flows):
    """Calculation of resultant enthalpy of mixing point between medium and low steam level turbine"""
    # Flow that comes from high and medium levels
    medium_enthalpy = medium_steam_turbine["outlet_enthalpy_real"]
    medium_flow = hrsg_flows["medium_steam"] + hrsg_flows["high_steam"]

    # Flow that comes directly from HRSG
    low_flow = hrsg_flows["low_steam"]

    # Calculating the result
    result_enthalpy = (medium_enthalpy * medium_flow + low_steam_enthalpy * low_flow) / (medium_flow + low_flow)
    return result_enthalpy

  def get_params_operation(self, input, saturation_parameters, entropy, enthalpy, medium_steam_turbine, hrsg_data, secant_method):
    """Calculation of params of operation of Low Level Steam Turbine"""
    # Getting resultant enthalpy of mixing point
    low_steam_enthalpy = enthalpy.overheated_steam(input.low_steam_level_pressure, input.low_steam_level_temperature)
    result_enthalpy = self.mixing_point_outlet_enthalpy(low_steam_enthalpy, medium_steam_turbine, hrsg_data["mass_flows"])

    # Getting steam inlet temperature of low steam turbine
    inlet_steam_temperature = secant_method.run(result_enthalpy, enthalpy, input.low_steam_level_pressure, saturation_parameters)

    # Intlet params
    efficiency = input.low_steam_level_efficiency
    inlet_enthalpy = result_enthalpy
    inlet_entropy = entropy.overheated_steam(input.low_steam_level_pressure, inlet_steam_temperature)

    # Calculation of the isentropic quality of the vapor at the outlet
    outlet_pressure = input.condenser_operation_pressure # Condenser pressure
    liquid_saturated_outlet_entropy = entropy.saturated_liquid(outlet_pressure)
    steam_saturated_outlet_entropy = entropy.saturated_steam(outlet_pressure)
    isentropic_quality_outlet_steam = (inlet_entropy - liquid_saturated_outlet_entropy) / (steam_saturated_outlet_entropy - liquid_saturated_outlet_entropy)

    # Calculation of isentropic enthalpy of outlet steam
    liquid_saturated_outlet_enthalpy = enthalpy.saturated_liquid(outlet_pressure)
    steam_saturated_outlet_enthalpy = enthalpy.saturated_steam(outlet_pressure)
    isentropic_enthalpy_outlet_steam = liquid_saturated_outlet_enthalpy + isentropic_quality_outlet_steam * (steam_saturated_outlet_enthalpy - liquid_saturated_outlet_enthalpy)
    delta_enthalpy_isentropic = isentropic_enthalpy_outlet_steam - inlet_enthalpy
    delta_enthalpy_real = delta_enthalpy_isentropic * (efficiency / 100)
    outlet_enthalpy_real = inlet_enthalpy + delta_enthalpy_real
    real_quality_outlet_steam = (outlet_enthalpy_real - liquid_saturated_outlet_enthalpy) / (steam_saturated_outlet_enthalpy - liquid_saturated_outlet_enthalpy)

    return {
      "delta_enthalpy_real": delta_enthalpy_real,
      "outlet_enthalpy_real": outlet_enthalpy_real,
      "real_quality_outlet_steam": real_quality_outlet_steam
      }
