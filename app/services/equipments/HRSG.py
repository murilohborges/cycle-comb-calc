import numpy as np

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

  def get_params_operation(self, input, enthalpy_calc, saturation_parameters, high_steam_turbine, pump):
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
    medium_steam_cold_enthaply = high_steam_turbine["outlet_enthalpy_real"]
    inlet_water_enthalpy = pump["outlet_real_enthalpy"]

    return {
      "high_steam_enthaply": high_steam_enthaply,
      "medium_steam_enthaply": medium_steam_enthaply,
      "low_steam_enthaply": low_steam_enthaply,
      "high_purge_enthalpy": high_purge_enthalpy,
      "medium_purge_enthalpy": medium_purge_enthalpy,
      "low_purge_enthalpy": low_purge_enthalpy,
      "medium_steam_cold_enthaply": medium_steam_cold_enthaply,
      "inlet_water_enthalpy": inlet_water_enthalpy
    }
  
  def get_mass_flow(self, input, hsrg_params, heat_supplied):
    """Calculation of mass flows in Heat Recovery Steam Generator (Steam generated, purge, boiler feed water) in kg/h"""
    # Getting steams and purge fractions
    high_steam_fraction = input.high_steam_level_fraction / 100
    medium_steam_fraction = input.medium_steam_level_fraction / 100
    low_steam_fraction = 1 - (high_steam_fraction + medium_steam_fraction)
    purge_fraction = input.purge_level / 100

    # Setting up the linear system of two equations (mass and energy balances) for the NumPy solver

    # ---Energy balance equation---
    # Coefficent of Steam total generated
    steam_coefficient_energy_balance = high_steam_fraction * hsrg_params["high_steam_enthaply"] + hsrg_params["medium_steam_enthaply"] * (high_steam_fraction + medium_steam_fraction) + low_steam_fraction * hsrg_params["low_steam_enthaply"] + purge_fraction * (high_steam_fraction * hsrg_params["high_purge_enthalpy"] + medium_steam_fraction * hsrg_params["medium_purge_enthalpy"] + low_steam_fraction * hsrg_params["low_purge_enthalpy"]) - high_steam_fraction * hsrg_params["medium_steam_cold_enthaply"]

    # Coefficent of boiler feed water
    feed_water_coefficient_energy_balance = -hsrg_params["inlet_water_enthalpy"]

    # Independent term
    independent_term_energy_balance = heat_supplied

    # ---Mass balance equation---
    # Coefficent of Steam total generated is just 1
    steam_coefficient_mass_balance = 1 + purge_fraction

    # Coefficent of boiler feed water is -1 too to equal steam total value
    feed_water_coefficient_mass_balance = -1

    # Independent term
    independent_term_mass_balance = 0 # There is no accumulation in the process

    # Coefficients matrix
    A = np.array([
      [steam_coefficient_energy_balance, feed_water_coefficient_energy_balance],
      [steam_coefficient_mass_balance, feed_water_coefficient_mass_balance]
    ], dtype=float)

    # Independents terms vector
    b = np.array([independent_term_energy_balance, independent_term_mass_balance], dtype=float)

    # Solving the linear system
    x = np.linalg.solve(A, b)
    total_steam_generated = x[0]
    feed_water_required = x[1]
    high_steam = total_steam_generated * high_steam_fraction
    medium_steam = total_steam_generated * medium_steam_fraction
    low_steam = total_steam_generated * low_steam_fraction
    purge = total_steam_generated * purge_fraction

    return {
      "total_steam_generated": total_steam_generated,
      "feed_water_required": feed_water_required,
      "high_steam": high_steam,
      "medium_steam": medium_steam,
      "low_steam": low_steam,
      "purge": purge
    }