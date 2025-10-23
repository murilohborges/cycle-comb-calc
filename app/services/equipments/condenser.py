from app.utils.errors import ThermodynamicError

class Condenser:
  """Service class to calculate properties of condenser"""
  def __init__(self):
    # Specific Heat Water value for the cooling and make-up water in the condenser
    self.specific_heat_water = 75.55
    # Temperature of Water value for the make-up water in the condenser in Celsius
    self.make_up_temperature_water = 25

  def get_params_operation(self, input, substance_repo, enthalpy, steam_turbine_hrsg_data):
    """Calculation of params of operation of condenser"""
    water_molar_mass = substance_repo.get_all()["water"]["molar_mass"]

    # Intern params
    operation_pressure = input.condenser_operation_pressure
    inlet_enthalpy = steam_turbine_hrsg_data["steam_turbine_data"]["low_steam_turbine_params"]["outlet_enthalpy_real"]
    steam_mass_flow = steam_turbine_hrsg_data["hrsg_data"]["mass_flows"]["total_steam_generated"]
    make_up_water_mass_flow = steam_turbine_hrsg_data["hrsg_data"]["mass_flows"]["purge"]
    outlet_enthalpy = enthalpy.saturated_liquid(operation_pressure)
    make_up_water_enthalpy = (self.specific_heat_water / water_molar_mass) * self.make_up_temperature_water # In kJ/kg

    # Checks operation pressure validation
    if operation_pressure <= 0:
      raise ThermodynamicError("Invalid condenser pressure: must be greater than zero.")

    # ---Mass balance equation---
    # Getting outlet flow mass of condenser (saturated liquid)
    outlet_mass_flow = steam_mass_flow + make_up_water_mass_flow

    # ---Energy balance equation (Hot side of condenser)---
    # Getting thermal change in kWatts
    thermal_change = (steam_mass_flow * inlet_enthalpy + make_up_water_mass_flow * make_up_water_enthalpy - outlet_mass_flow * outlet_enthalpy) / 3600 # In kW

    # ---Energy balance equation (Cooling water of condenser)---
    delta_cooling_water_temperature = input.range_temperature_cooling_tower
    cooling_water_mass_flow = ((thermal_change * 3600) / (delta_cooling_water_temperature * (self.specific_heat_water / water_molar_mass))) / 1000 # in ton/h

    return {
      "thermal_change": thermal_change,
      "cooling_water_mass_flow": cooling_water_mass_flow,
      "make_up_water_mass_flow": make_up_water_mass_flow,
      "saturated_water_mass_flow": outlet_mass_flow
    }
