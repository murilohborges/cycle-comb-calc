from ..thermodynamics.steam.enthalpy import Enthalpy
from ..thermodynamics.steam.entropy import Entropy
from ..thermodynamics.steam.specific_volume import SpecificVolume
from ..thermodynamics.steam.saturation_parameters import SaturationParameters
from ..thermodynamics.heat.icph import ICPH
from ..equipments.HRSG import HRSG
from ..equipments.high_steam_turbine import HighSteamTurbine
from ..equipments.medium_steam_turbine import MediumSteamTurbine
from ..equipments.low_steam_turbine import LowSteamTurbine
from ..equipments.condenser import Condenser
from ..equipments.pump import Pump
from ..utils.secant_method import SecantMethod

class RankineCycle:
  """Service class of all methods and calculations related to Rankine's cycle"""
  def __init__(self, input, substance_repo, icph_repo, heat_suplier_cycle):
    self.input = input
    self.substance_repo = substance_repo
    self.icph_repo = icph_repo
    self.heat_suplier_cycle = heat_suplier_cycle
    self.enthalpy = Enthalpy()
    self.entropy = Entropy()
    self.specific_volume = SpecificVolume()
    self.icph = ICPH()
    self.hrsg = HRSG()
    self.saturation_parameters = SaturationParameters()
    self.high_steam_turbine = HighSteamTurbine()
    self.medium_steam_turbine = MediumSteamTurbine()
    self.low_steam_turbine = LowSteamTurbine()
    self.pump = Pump()
    self.condenser = Condenser()
    self.secant_method = SecantMethod()
  
  def hrsg_and_steam_turbine(self):
    """Calculation of operation params of HRSG and All levels of Steam Turbine"""
    # Due to the high coupling of logic between these two cycle equipment, their calculations are made in a single object.
    # Getting first operation conditions of high and medium steam turbine, so we can get all data of HRSG
    high_steam_turbine_params = self.high_steam_turbine.get_params_operation(self.input, self.saturation_parameters, self.entropy, self.enthalpy, self.secant_method)
    medium_steam_turbine_params = self.medium_steam_turbine.get_params_operation(self.input, self.saturation_parameters, self.entropy, self.enthalpy, self.secant_method)

    # Calculating operation conditions and properties of HRSG
    heat_suplied_hrsg = self.hrsg.heat_supplied_calc(self.input, self.heat_suplier_cycle["combustion_gas"], self.heat_suplier_cycle["exhaustion_temp"], self.icph)
    hrsg_params = self.hrsg.get_params_operation(self.input, self.enthalpy, self.saturation_parameters, high_steam_turbine_params, self.pump_calc()["params_operation"])
    hrsg_mass_flows = self.hrsg.get_mass_flow(self.input, hrsg_params, heat_suplied_hrsg)
    hrsg_data = {
      "heat_suplied_hrsg": heat_suplied_hrsg,
      "params": hrsg_params,
      "mass_flows": hrsg_mass_flows
    }

    # Calculation of low steam turbine
    low_steam_turbine_params = self.low_steam_turbine.get_params_operation(self.input, self.saturation_parameters, self.entropy, self.enthalpy, medium_steam_turbine_params, hrsg_data, self.secant_method)

    # Organizing steam turbine data
    steam_turbine_data = {
      "high_steam_turbine_params": high_steam_turbine_params,
      "medium_steam_turbine_params": medium_steam_turbine_params,
      "low_steam_turbine_params": low_steam_turbine_params
    }
    
    return {
      "hrsg_data": hrsg_data,
      "steam_turbine_data": steam_turbine_data
    }
  
  def condenser_calc(self):
    """Calculation of operation params of Condenser"""
    params_operation = self.condenser.get_params_operation(self.input, self.substance_repo, self.enthalpy, self.saturation_parameters, self.hrsg_and_steam_turbine())
    return params_operation
  
  def pump_calc(self):
    """Calculation of operation params of Pump"""
    params_operation = self.pump.get_params_operation(self.input, self.enthalpy, self.specific_volume, self.saturation_parameters)
    return {
      "params_operation": params_operation
    }
  
  
  def run(self):
    """Executing all logic sequence of calculation of Rankine Cycle"""
    # Getting HRSG and Steam Turbine data
    hrsg_data = self.hrsg_and_steam_turbine()["hrsg_data"]
    steam_turbine_data = self.hrsg_and_steam_turbine()["steam_turbine_data"]

    # Getting Pump data
    pump_data = self.pump_calc()

    # Getting Condenser data
    condenser_data = self.condenser_calc()

    return {
      "hrsg_data": hrsg_data,
      "steam_turbine_data": steam_turbine_data,
      "pump_data": pump_data,
      "condenser_data": condenser_data
    }