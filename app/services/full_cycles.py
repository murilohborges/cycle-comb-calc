from collections import namedtuple

# Tuple test
FullCycleResult = namedtuple("FullCycleResult", [
    "PCI_fuel", "air_mass_flow", "exhaustion_gas_tempature",
    "exhaustion_gas_mass_flow", "thermal_charge", "saturated_water_mass_flow",
    "make_up_water_mass_flow", "cooling_water_mass_flow", "quality_exhaustion_steam_turbine",
    "high_steam_mass_flow", "medium_steam_mass_flow", "low_steam_mass_flow",
    "pump_variation_pressure", "net_power_gas_turbine", "gross_power_steam_turbine",
    "net_power_steam_turbine", "power_consumed_pump", "gross_power_cycle_combined",
    "net_power_cycle_combined", "gross_cycle_combined", "net_cycle_combined"
])

class FullCycle:
  
  def create_full_cycles_combined():
    result_of_cycles = FullCycleResult(
      PCI_fuel=1.0,
      air_mass_flow=1.0,
      exhaustion_gas_tempature=1.0,
      exhaustion_gas_mass_flow=1.0,
      thermal_charge=1.0,
      saturated_water_mass_flow=1.0,
      make_up_water_mass_flow=1.0,
      cooling_water_mass_flow=1.0,
      quality_exhaustion_steam_turbine=1.0,
      high_steam_mass_flow=1.0,
      medium_steam_mass_flow=1.0,
      low_steam_mass_flow=1.0,
      pump_variation_pressure=1.0,
      net_power_gas_turbine=1.0,
      gross_power_steam_turbine=1.0,
      net_power_steam_turbine=1.0,
      power_consumed_pump=1.0,
      gross_power_cycle_combined=1.0,
      net_power_cycle_combined=1.0,
      gross_cycle_combined=50.0,
      net_cycle_combined=50.0
    )
    return result_of_cycles