from collections import namedtuple
from ..equipments.gas_turbine import GasTurbine
from ..chemistry.gas_fuel import GasFuel
from ...repositories.repositories_container import RepositoriesContainer
from ..thermodynamics.steam.saturation_parameters import SaturationParameters

# Tuple test
FullCyclesResult = namedtuple("FullCyclesResult", [
    "LHV_fuel", "air_mass_flow", "exhaustion_gas_tempature",
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
    self.gas_fuel = GasFuel(
      input, 
      substance_repo=repositories.substance_repository,
      icph_repo=repositories.icph_repository
    )
    self.gas_turbine = GasTurbine(
      input,
      gas_fuel=self.gas_fuel,
      substance_repo=repositories.substance_repository,
      icph_repo=repositories.icph_repository
    )
  
  def create_full_cycles_combined(self):
    """
    Orchestrator of all calculation in Cycles Combined
    """
    # All logic of Gas Turbine
    LHV_fuel = self.gas_fuel.LHV_fuel_calc()
    net_power_gas_turbine = self.gas_turbine.net_power_GT_calculation()
    air_mass_flow = self.gas_turbine.input_air_mass_flow()
    # print(f"tsat")
    
    
    result_of_cycles = FullCyclesResult(
      LHV_fuel= round(LHV_fuel, 2),
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