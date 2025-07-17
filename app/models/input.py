from pydantic import BaseModel

class Input(BaseModel):
  """
    All variables for calculations
  """
  # Fuel Composition
  methane_molar_fraction_fuel: float
  ethane_molar_fraction_fuel: float
  propane_molar_fraction_fuel: float
  butane_molar_fraction_fuel: float
  water_molar_fraction_fuel: float
  carbon_dioxide_molar_fraction_fuel: float
  hydrogen_molar_fraction_fuel: float
  nitrogen_molar_fraction_fuel: float

  # Gas turbine specifications (Brayton Cycle)
  fuel_mass_flow: float
  fuel_input_temperature: float
  air_input_temperature: float
  percent_excess_air: float
  local_atmospheric_pressure: float
  relative_humity: float
  gas_turbine_efficiency: float
  chimney_gas_temperature: float

  # Heat Recovery Steam Generation (HRSG) specifications (Rankine Cycle)
  purge_level: float
  high_steam_level_pressure: float
  medium_steam_level_pressure: float
  low_steam_level_pressure: float
  high_steam_level_temperature: float
  medium_steam_level_temperature: float
  low_steam_level_temperature: float
  high_steam_level_fraction: float
  medium_steam_level_fraction: float

  # Steam turbine specifications (Rankine Cycle)
  high_steam_level_efficiency: float
  medium_steam_level_efficiency: float
  low_steam_level_efficiency: float
  reductor_generator_set_efficiency: float

  # Pump specifications (Rankine Cycle)
  pump_efficiency: float
  engine_pump_efficiency: float
  power_factor_pump_efficiency: float

  # Condenser specifications (Rankine Cycle)
  condenser_operation_pressure: float
  range_temperature_cooling_tower: float