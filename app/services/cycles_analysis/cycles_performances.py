class CyclesPerformances():
  """Service class of all methods and calculations related to Cycles combined's permances"""
  def cycles_effiencies_calc(self, input, net_power_gas_turbine, LHV_fuel, fuel_sensible_heat, rankine_cycle_data):
    """Calculation of cycles effciencies"""
    # Getting gross and net power of combined cycles (Brayton-Rankine)
    gross_power_combined_cycles = net_power_gas_turbine + rankine_cycle_data["net_power_steam_turbine"]
    net_power_combined_cycles = gross_power_combined_cycles - rankine_cycle_data["consumed_power"]

    # Getting gross and net efficiencies of full combined cycles
    fuel_mass_flow = input.fuel_mass_flow
    gross_cycle_combined_efficiency = (gross_power_combined_cycles / (fuel_mass_flow * (LHV_fuel + abs(fuel_sensible_heat)) * (1/3600))) * 100
    net_cycle_combined_efficiency = (net_power_combined_cycles / (fuel_mass_flow * (LHV_fuel + abs(fuel_sensible_heat)) * (1/3600))) * 100
    return {
      "gross_power_combined_cycles": gross_power_combined_cycles,
      "net_power_combined_cycles": net_power_combined_cycles,
      "gross_cycle_combined_efficiency": gross_cycle_combined_efficiency,
      "net_cycle_combined_efficiency": net_cycle_combined_efficiency
    }