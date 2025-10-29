from pydantic import BaseModel, Field

class Output(BaseModel):
  """
  All results of calculations
  """
  # Gas turbine (Brayton Cycle)
  LHV_fuel: float = Field(..., gt=0, description="Lower Heating Value of the fuel (kJ/kg)")
  air_mass_flow: float = Field(..., gt=0, description="Mass flow rate of air entering the gas turbine (kg/h)")
  exhaustion_gas_temperature: float = Field(..., gt=0, description="Temperature of the gas exiting the turbine (°C)")
  exhaustion_gas_mass_flow: float = Field(..., gt=0, description="Mass flow rate of exhaust gases (kg/h)")

  # Condenser (Rankine Cycle)
  thermal_charge: float = Field(..., gt=0, description="Thermal energy transferred to the condenser (kW)")
  saturated_water_mass_flow: float = Field(..., gt=0, description="Mass flow rate of saturated water leaving the condenser (kg/h)")
  make_up_water_mass_flow: float = Field(..., ge=0, description="Mass flow rate of make-up water added to the system (kg/h)")
  cooling_water_mass_flow: float = Field(..., gt=0, description="Mass flow rate of cooling water in the condenser (t/h)")
  quality_exhaustion_steam_turbine: float = Field(..., gt=0, description="Steam quality at the turbine exhaust (fraction or %)")

  # Heat Recovery Steam Generation (HRSG - Rankine Cycle)
  high_steam_mass_flow: float = Field(..., gt=0, description="Mass flow rate of high-pressure steam (kg/h)")
  medium_steam_mass_flow: float = Field(..., gt=0, description="Mass flow rate of medium-pressure steam (kg/h)")
  low_steam_mass_flow: float = Field(..., gt=0, description="Mass flow rate of low-pressure steam (kg/h)")
  pump_variation_pressure: float = Field(..., gt=0, description="Pressure increase provided by the feedwater pump (bar a.)")

  # Electrical powers generated
  net_power_gas_turbine: float = Field(..., gt=0, description="Net electrical power produced by the gas turbine (kW)")
  gross_power_steam_turbine: float = Field(..., gt=0, description="Gross electrical power produced by the steam turbine (kW)")
  net_power_steam_turbine: float = Field(..., gt=0, description="Net electrical power of the steam turbine after auxiliary consumption (kW)")
  power_consumed_pump: float = Field(..., gt=0, description="Power consumed by all pumps in the Rankine cycle (kW)")
  gross_power_cycle_combined: float = Field(..., gt=0, description="Gross power of the combined cycle (kW)")
  net_power_cycle_combined: float = Field(..., gt=0, description="Net power of the combined cycle after all auxiliary consumption (kW)")

  # Efficiencies of Cycle Combined
  gross_cycle_combined_efficiency: float = Field(..., gt=0, le=100, description="Gross efficiency of the combined cycle (%)")
  net_cycle_combined_efficiency: float = Field(..., gt=0, le=100, description="Net efficiency of the combined cycle (%)")
