from pydantic import BaseModel

class Output(BaseModel):
  """
    All results of calculations
  """
  # Gas turbine (Brayton Cycle)
  PCI_fuel: float
  air_mass_flow: float
  exaustion_gas_tempature: float
  exaustion_gas_mass_flow: float

  # Heat Recovery Steam Generation (HRSG - Rankine Cycle)
  high_steam_mass_flow: float
  medium_steam_mass_flow: float
  low_steam_mass_flow: float
  pump_variation_pressure: float

  # Electrical powers generated
  net_power_gas_turbine: float
  gross_power_steam_turbine: float
  net_power_steam_turbine: float
  power_consumed_pump: float
  gross_power_cycle_combined: float
  net_power_cycle_combined: float

  # Efficiencies of Cycle Combined
  gross_cycle_combined: float
  net_cycle_combined: float