from pydantic import BaseModel, Field

class Input(BaseModel):
  """
  All variables for calculations
  """
  # Fuel Composition
  methane_molar_fraction_fuel: float = Field(..., le=100, ge=0, example=90, description="Molar fraction in percentage (%)")
  ethane_molar_fraction_fuel: float = Field(..., le=100, ge=0, example=0, description="Molar fraction in percentage (%)")
  propane_molar_fraction_fuel: float = Field(..., le=100, ge=0, example=0, description="Molar fraction in percentage (%)")
  n_butane_molar_fraction_fuel: float = Field(..., le=100, ge=0, example=0, description="Molar fraction in percentage (%)")
  water_molar_fraction_fuel: float = Field(..., le=100, ge=0, example=0, description="Molar fraction in percentage (%)")
  carbon_dioxide_molar_fraction_fuel: float = Field(..., le=100, ge=0, example=5, description="Molar fraction in percentage (%)")
  hydrogen_molar_fraction_fuel: float = Field(..., le=100, ge=0, example=0, description="Molar fraction in percentage (%)")
  nitrogen_molar_fraction_fuel: float = Field(..., le=100, ge=0, example=5, description="Molar fraction in percentage (%)")

  # Gas turbine specifications (Brayton Cycle)
  fuel_mass_flow: float = Field(..., gt=0, example=50000, description="Mass flow rate in kg/h")
  fuel_input_temperature: float = Field(..., le=1226.85, ge=24.85, example=25.0, description="Fuel input temperature in °C")
  air_input_temperature: float = Field(..., le=1226.85, ge=24.85, example=25.0, description="Air input temperature in °C")
  percent_excess_air: float = Field(..., ge=0, example=150, description="percentage of excess air (%)")
  local_atmospheric_pressure: float = Field(..., le=1, gt = 0.9, example=1, description="Local atmospheric pressure in atm")
  local_temperature: float = Field(..., le=50, gt = 5, example=15, description="Local temperature in °C")
  relative_humidity: float = Field(..., le=100, ge=0, example=60, description="Local relative humidity in percentage (%)")
  gas_turbine_efficiency: float = Field(..., le=50, ge=10, example=37.5, description="Gas turbine efficiency in percentage (%)")
  chimney_gas_temperature: float = Field(..., le=200, ge=80, example=100, description="Chimney gas temperature in °C")

  # Heat Recovery Steam Generation (HRSG) specifications (Rankine Cycle)
  purge_level: float = Field(..., le=10, ge=0, example=5.0, description="Purge percentage in percentage (%)")
  high_steam_level_pressure: float = Field(..., le=220, ge=1.01325, example=98, description="High steam level pressure in bar a.")
  medium_steam_level_pressure: float = Field(..., le=220, ge=1.01325, example=24, description="Medium steam level pressure in bar a.")
  low_steam_level_pressure: float = Field(..., le=220, ge=1.01325, example=4, description="Low steam level pressure in bar a.")
  high_steam_level_temperature: float = Field(..., le=620, example=565, description="High steam level temperature in °C")
  medium_steam_level_temperature: float = Field(..., le=620, example=565, description="Medium steam level temperature in °C")
  low_steam_level_temperature: float = Field(..., le=620, example=312.5, description="Low steam level temperature in °C")
  high_steam_level_fraction: float = Field(..., lt=100, gt=0, example=70, description="High steam level fraction in percentage (%)")
  medium_steam_level_fraction: float = Field(..., lt=100, gt=0, example=15, description="Low steam level fraction in percentage (%)")

  # Steam turbine specifications (Rankine Cycle)
  high_steam_level_efficiency: float = Field(..., le=100, gt=0, example=89, description="High steam level efficiency in percentage (%)")
  medium_steam_level_efficiency: float = Field(..., le=100, gt=0, example=90, description="Medium steam level efficiency in percentage (%)")
  low_steam_level_efficiency: float = Field(..., le=100, gt=0, example=91, description="Low steam level efficiency in percentage (%)")
  reductor_generator_set_efficiency: float = Field(..., le=100, gt=0, example=90, description="Reductor/Generator set efficiency in percentage (%)")

  # Pump specifications (Rankine Cycle)
  pump_efficiency: float = Field(..., le=100, gt=0, example=75.0, description="Pump efficiency in percentage (%)")
  engine_pump_efficiency: float = Field(..., le=100, gt=0, example=80.0, description="Pump engine efficiency in percentage (%)")
  power_factor_pump_efficiency: float = Field(..., le=1, gt=0, example=0.84, description="Power factor pump efficiency between 0 and 1")

  # Condenser specifications (Rankine Cycle)
  condenser_operation_pressure: float = Field(..., ge=0, le=1.01325, example=0.074, description="Condenser operation pressure in bar a.")
  range_temperature_cooling_tower: float = Field(..., ge=5, le=15, example=10, description="Range cooling tower temperature in °C")
