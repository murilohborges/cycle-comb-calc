from pydantic import BaseModel, Field

class Output(BaseModel):
  """
    All results of calculations
  """
  # Gas turbine (Brayton Cycle)
  PCI_fuel: float = Field(..., gt=0)
  air_mass_flow: float = Field(..., gt=0)
  exhaustion_gas_tempature: float = Field(..., gt=0)
  exhaustion_gas_mass_flow: float = Field(..., gt=0)

  # Condenser (Rankine Cycle)
  thermal_charge: float = Field(..., gt=0)
  saturated_water_mass_flow: float = Field(..., gt=0)
  make_up_water_mass_flow: float = Field(..., gt=0)
  cooling_water_mass_flow: float = Field(..., gt=0)
  quality_exhaustion_steam_turbine: float = Field(..., gt=0)

  # Heat Recovery Steam Generation (HRSG - Rankine Cycle)
  high_steam_mass_flow: float = Field(..., gt=0)
  medium_steam_mass_flow: float = Field(..., gt=0)
  low_steam_mass_flow: float = Field(..., gt=0)
  pump_variation_pressure: float = Field(..., gt=0)

  # Electrical powers generated
  net_power_gas_turbine: float = Field(..., gt=0)
  gross_power_steam_turbine: float = Field(..., gt=0)
  net_power_steam_turbine: float = Field(..., gt=0)
  power_consumed_pump: float = Field(..., gt=0)
  gross_power_cycle_combined: float = Field(..., gt=0)
  net_power_cycle_combined: float = Field(..., gt=0)

  # Efficiencies of Cycle Combined
  gross_cycle_combined: float = Field(..., gt=0, le=100)
  net_cycle_combined: float = Field(..., gt=0, le=100)