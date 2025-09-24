class Pump:
  """Service class to calculate properties of outlet water pump"""
  def get_params_operation(self, input, enthalpy, specific_volume, saturation_params):
    """Calculation of params of operation of outlet water pump"""
    # Pump outlet pressure set at 20 bar above the high level vapor pressure value, as a guarantee that it is not in violation of the Second Law of Thermodynamics
    outlet_pressure = input.high_steam_level_pressure + 20

    # Inlet pressure is the same of the condenser operation 
    inlet_pressure = input.condenser_operation_pressure
    inlet_real_enthalpy = enthalpy.saturated_liquid(inlet_pressure, saturation_params)

    # Delta pressure calculation and converting from Bar to Pascal
    delta_pressure = (outlet_pressure - inlet_pressure) * 100000

    # Outlet real enthalpy by pump efficency and converting from J/kg to kJ/kg
    outlet_real_enthalpy = ((specific_volume.saturated_liquid(inlet_pressure, saturation_params) * delta_pressure * 0.001) / (input.pump_efficiency / 100)) + inlet_real_enthalpy

    return {
      "outlet_real_enthalpy": outlet_real_enthalpy,
      "delta_pressure": delta_pressure / 100000 # in bar
    }