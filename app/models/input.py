from pydantic import BaseModel, Field

class Input(BaseModel):
  """
  All variables for calculations
  """
  # Fuel Composition
  methane_molar_fraction_fuel: float = Field(..., le=100, ge=0)
  ethane_molar_fraction_fuel: float = Field(..., le=100, ge=0)
  propane_molar_fraction_fuel: float = Field(..., le=100, ge=0)
  n_butane_molar_fraction_fuel: float = Field(..., le=100, ge=0)
  water_molar_fraction_fuel: float = Field(..., le=100, ge=0)
  carbon_dioxide_molar_fraction_fuel: float = Field(..., le=100, ge=0)
  hydrogen_molar_fraction_fuel: float = Field(..., le=100, ge=0)
  nitrogen_molar_fraction_fuel: float = Field(..., le=100, ge=0)

  # Gas turbine specifications (Brayton Cycle)
  fuel_mass_flow: float = Field(..., gt=0)
  fuel_input_temperature: float = Field(..., le=1226.85, ge=24.85)
  air_input_temperature: float = Field(..., le=1226.85, ge=24.85)
  percent_excess_air: float = Field(..., ge=0)
  local_atmospheric_pressure: float = Field(..., le=1, gt = 0.9)
  relative_humity: float = Field(..., le=100, ge=0)
  gas_turbine_efficiency: float = Field(..., le=50, ge=10)
  chimney_gas_temperature: float = Field(..., le=200, ge=80)

  # Heat Recovery Steam Generation (HRSG) specifications (Rankine Cycle)
  purge_level: float = Field(..., le=10, ge=0)
  high_steam_level_pressure: float = Field(..., le=220, ge=1.01325)
  medium_steam_level_pressure: float = Field(..., le=220, ge=1.01325)
  low_steam_level_pressure: float = Field(..., le=220, ge=1.01325)
  high_steam_level_temperature: float = Field(..., le=620)
  medium_steam_level_temperature: float = Field(..., le=620)
  low_steam_level_temperature: float = Field(..., le=620)
  high_steam_level_fraction: float = Field(..., lt=100, gt=0)
  medium_steam_level_fraction: float = Field(..., lt=100, gt=0)

  # Steam turbine specifications (Rankine Cycle)
  high_steam_level_efficiency: float = Field(..., le=100, gt=0)
  medium_steam_level_efficiency: float = Field(..., le=100, gt=0)
  low_steam_level_efficiency: float = Field(..., le=100, gt=0)
  reductor_generator_set_efficiency: float = Field(..., le=100, gt=0)

  # Pump specifications (Rankine Cycle)
  pump_efficiency: float = Field(..., le=100, gt=0)
  engine_pump_efficiency: float = Field(..., le=100, gt=0)
  power_factor_pump_efficiency: float = Field(..., le=1, gt=0)

  # Condenser specifications (Rankine Cycle)
  condenser_operation_pressure: float = Field(..., ge=0, le=1.01325)
  range_temperature_cooling_tower: float = Field(..., ge=5, le=15)
