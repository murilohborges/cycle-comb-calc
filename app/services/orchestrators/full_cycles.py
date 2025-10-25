from collections import namedtuple
from ...repositories.repositories_container import RepositoriesContainer
from .brayton_cycle import BraytonCycle
from .rankine_cycle import RankineCycle
from ..cycles_analysis.cycles_performances import CyclesPerformances

# Tuple of the result
FullCyclesResult = namedtuple("FullCyclesResult", [
    "LHV_fuel", "air_mass_flow", "exhaustion_gas_temperature",
    "exhaustion_gas_mass_flow", "thermal_charge", "saturated_water_mass_flow",
    "make_up_water_mass_flow", "cooling_water_mass_flow", "quality_exhaustion_steam_turbine",
    "high_steam_mass_flow", "medium_steam_mass_flow", "low_steam_mass_flow",
    "pump_variation_pressure", "net_power_gas_turbine", "gross_power_steam_turbine",
    "net_power_steam_turbine", "power_consumed_pump", "gross_power_cycle_combined",
    "net_power_cycle_combined", "gross_cycle_combined_efficiency", "net_cycle_combined_efficiency"
])

class FullCycles:
  def __init__(self, input, repositories: RepositoriesContainer):
    self.input = input
    self.substance_repo = repositories.substance_repository
    self.icph_repo = repositories.icph_repository
    self.brayton_cycle = BraytonCycle(self.input, self.substance_repo, self.icph_repo)
    self.cycles_performances= CyclesPerformances()

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
    fuel_sensible_heat = brayton_cycle_data["fuel_sensible_heat"]

    # All logic of Rankine Cycle
    rankine_cycle_data = RankineCycle(self.input, self.substance_repo, self.icph_repo, heat_suplier_cycle=brayton_cycle_data).run()
    hrsg_data = rankine_cycle_data["hrsg_data"]
    pump_data = rankine_cycle_data["pump_data"]
    steam_turbine_data = rankine_cycle_data["steam_turbine_data"]
    condenser_data = rankine_cycle_data["condenser_data"]
    generated_consumed_powers_data = rankine_cycle_data["generated_consumed_powers_data"]

    # All logic of Performance Cycles Calculation
    # Getting cycles performances data
    cycles_performances_data = self.cycles_performances.cycles_effiencies_calc(self.input, net_power_gas_turbine, LHV_fuel, fuel_sensible_heat, rankine_cycle_data["generated_consumed_powers_data"])

    result_of_cycles = FullCyclesResult(
      LHV_fuel = round(LHV_fuel, 2),
      air_mass_flow = round(input_air_porperties["mass_flow"], 2),
      exhaustion_gas_temperature = round(exhaustion_gas_temperature, 2),
      exhaustion_gas_mass_flow = round(combustion_gas_properties["mass_flow"], 2),
      thermal_charge = round(condenser_data["thermal_change"], 2),
      saturated_water_mass_flow = round(condenser_data["saturated_water_mass_flow"], 2),
      make_up_water_mass_flow = round(condenser_data["make_up_water_mass_flow"], 2),
      cooling_water_mass_flow = round(condenser_data["cooling_water_mass_flow"], 2),
      quality_exhaustion_steam_turbine = round(steam_turbine_data["low_steam_turbine_params"]["real_quality_outlet_steam"], 2),
      high_steam_mass_flow = round(hrsg_data["mass_flows"]["high_steam"], 2),
      medium_steam_mass_flow = round(hrsg_data["mass_flows"]["medium_steam"], 2),
      low_steam_mass_flow = round(hrsg_data["mass_flows"]["low_steam"], 2),
      pump_variation_pressure = round(pump_data["params_operation"]["delta_pressure"], 2),
      net_power_gas_turbine= round(net_power_gas_turbine, 2),
      gross_power_steam_turbine = round(generated_consumed_powers_data["gross_power_steam_turbine"], 2),
      net_power_steam_turbine = round(generated_consumed_powers_data["net_power_steam_turbine"], 2),
      power_consumed_pump = round(generated_consumed_powers_data["consumed_power"], 2),
      gross_power_cycle_combined = round(cycles_performances_data["gross_power_combined_cycles"], 2),
      net_power_cycle_combined = round(cycles_performances_data["net_power_combined_cycles"], 2),
      gross_cycle_combined_efficiency = round(cycles_performances_data["gross_cycle_combined_efficiency"], 2),
      net_cycle_combined_efficiency = round(cycles_performances_data["net_cycle_combined_efficiency"], 2)
    )
    return result_of_cycles
