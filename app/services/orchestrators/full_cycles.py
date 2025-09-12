from collections import namedtuple
from ...repositories.repositories_container import RepositoriesContainer
from .brayton_cycle import BraytonCycle
from .rankine_cycle import RankineCycle

# Tuple test
FullCyclesResult = namedtuple("FullCyclesResult", [
    "LHV_fuel", "air_mass_flow", "exhaustion_gas_temperature",
    "exhaustion_gas_mass_flow", "thermal_charge", "saturated_water_mass_flow",
    "make_up_water_mass_flow", "cooling_water_mass_flow", "quality_exhaustion_steam_turbine",
    "high_steam_mass_flow", "medium_steam_mass_flow", "low_steam_mass_flow",
    "pump_variation_pressure", "net_power_gas_turbine", "gross_power_steam_turbine",
    "net_power_steam_turbine", "power_consumed_pump", "gross_power_cycle_combined",
    "net_power_cycle_combined", "gross_cycle_combined", "net_cycle_combined"
])

# Tuple input test
FullCyclesInput = namedtuple("FullCyclesInput", [
    "methane_molar_fraction_fuel", "ethane_molar_fraction_fuel", "propane_molar_fraction_fuel",
    "butane_molar_fraction_fuel", "water_molar_fraction_fuel", "carbon_dioxide_molar_fraction_fuel",
    "hydrogen_molar_fraction_fuel", "nitrogen_molar_fraction_fuel", "fuel_mass_flow",
    "fuel_input_temperature", "air_input_temperature", "percent_excess_air",
    "local_atmospheric_pressure", "relative_humity", "gas_turbine_efficiency",
    "chimney_gas_temperature", "purge_level", "high_steam_level_pressure",
    "medium_steam_level_pressure", "low_steam_level_pressure", "high_steam_level_temperature", "medium_steam_level_temperature", "low_steam_level_temperature", "high_steam_level_fraction", "medium_steam_level_fraction", "high_steam_level_efficiency", "medium_steam_level_efficiency", "low_steam_level_efficiency", "reductor_generator_set_efficiency", "pump_efficiency", "engine_pump_efficiency", "power_factor_pump_efficiency", "condenser_operation_pressure", "range_temperature_cooling_tower"
])


class FullCycles:
  def __init__(self, input, repositories: RepositoriesContainer):
    self.input = input
    self.substance_repo = repositories.substance_repository
    self.icph_repo = repositories.icph_repository
    self.brayton_cycle = BraytonCycle(self.input, self.substance_repo, self.icph_repo)
    self.rankine_cycle = RankineCycle(self.input, self.substance_repo, self.icph_repo)

  def create_full_cycles_combined(self):
    """
    Orchestrator of all calculation in Cycles Combined
    """
    # All logic of Brayton Cycle
    brayton_cycle_data = self.brayton_cycle.run()
    LHV_fuel = brayton_cycle_data["LHV_fuel"]
    net_power_gas_turbine = brayton_cycle_data["net_power"]
    input_air_porperties = brayton_cycle_data["input_air"]
    combustion_gas_properties = brayton_cycle_data["combustion_gas"]
    exhaustion_gas_temperature = brayton_cycle_data["exhaustion_temp"]

    # All logic of Rankine Cycle
    rankine_cycle_data = self.rankine_cycle.HRSG_calc()
    


    result_of_cycles = FullCyclesResult(
      LHV_fuel = round(LHV_fuel, 2),
      air_mass_flow = round(input_air_porperties["mass_flow"], 2),
      exhaustion_gas_temperature = round(exhaustion_gas_temperature, 2),
      exhaustion_gas_mass_flow = round(combustion_gas_properties["mass_flow"] ,2),
      thermal_charge=1.0,
      saturated_water_mass_flow=1.0,
      make_up_water_mass_flow=1.0,
      cooling_water_mass_flow=1.0,
      quality_exhaustion_steam_turbine=1.0,
      high_steam_mass_flow=1.0,
      medium_steam_mass_flow=1.0,
      low_steam_mass_flow=1.0,
      pump_variation_pressure=1.0,
      net_power_gas_turbine= round(net_power_gas_turbine, 2),
      gross_power_steam_turbine=1.0,
      net_power_steam_turbine=1.0,
      power_consumed_pump=1.0,
      gross_power_cycle_combined=1.0,
      net_power_cycle_combined=1.0,
      gross_cycle_combined=50.0,
      net_cycle_combined=50.0
    )
    return result_of_cycles
