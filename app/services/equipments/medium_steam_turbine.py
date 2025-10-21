from app.utils.errors import ThermodynamicError

class MediumSteamTurbine:
  """Service class to calculate properties of medium pressure steam turbine"""
  def get_params_operation(self, input, saturation_parameters, entropy, enthalpy, secant_method):
    """Calculation of params of operation of Medium Level Steam Turbine"""
    efficiency = input.medium_steam_level_efficiency
    saturation_temperature = round(saturation_parameters.saturation_temperature(input.medium_steam_level_pressure), 2)

    # Before calculating, checks if the temperature of the steam is above saturation, so the secant method can converge
    # This verification is crucial for the HRSG's calculations, so it is made in this module too
    if input.medium_steam_level_temperature <= saturation_temperature:
      raise ThermodynamicError(f"The medium steam temperature is below saturation ({saturation_temperature}°C)")

    # Inlet params
    inlet_entropy = entropy.overheated_steam(input.medium_steam_level_pressure, input.medium_steam_level_temperature)
    inlet_enthalpy = enthalpy.overheated_steam(input.medium_steam_level_pressure, input.medium_steam_level_temperature)

    # Estimating outlet enthalpy of process isentropic
    outlet_temperature_isentropic = secant_method.run(inlet_entropy, entropy, input.low_steam_level_pressure, saturation_parameters)
    outlet_enthalpy_isentropic = enthalpy.overheated_steam(input.low_steam_level_pressure, outlet_temperature_isentropic)

    # Estimating real outlet enthalpy
    delta_enthalpy_isentropic = outlet_enthalpy_isentropic - inlet_enthalpy
    delta_enthalpy_real = delta_enthalpy_isentropic * (efficiency/100)
    outlet_enthalpy_real = inlet_enthalpy + delta_enthalpy_real

    return {
      "delta_enthalpy_real": delta_enthalpy_real,
      "outlet_enthalpy_real": outlet_enthalpy_real
      }
