from ..thermodynamics.steam.enthalpy import Enthalpy
from ..thermodynamics.steam.entropy import Entropy
from ..thermodynamics.steam.specific_volume import SpecificVolume
from ..thermodynamics.steam.saturation_parameters import SaturationParameters
from ..thermodynamics.heat.icph import ICPH
from ..equipments.HRSG import HRSG
from ..equipments.high_steam_turbine import HighSteamTurbine
from ..equipments.pump import Pump
from ..utils.secant_method import SecantMethod

class RankineCycle:
  """Service class of all methods and calculations related to Rankine's cycle"""
  def __init__(self, input, substance_repo, icph_repo):
    self.input = input
    self.substance_repo = substance_repo
    self.icph_repo = icph_repo
    self.enthalpy = Enthalpy()
    self.entropy = Entropy()
    self.specific_volume = SpecificVolume()
    self.icph = ICPH()
    self.hrsg = HRSG()
    self.saturation_parameters = SaturationParameters()
    self.high_steam_turbine = HighSteamTurbine()
    self.pump = Pump()
    self.secant_method = SecantMethod()
  
  def HRSG_calc(self, brayton_cycle_data):
    """Calculating operation conditions and properties of HRSG"""
    heat_suplied_hrsg = self.hrsg.heat_supplied_calc(self.input, brayton_cycle_data["combustion_gas"], brayton_cycle_data["exhaustion_temp"], self.icph)
    
    hrsg_params = self.hrsg.get_params_operation(self.input, self.enthalpy, self.saturation_parameters, self.steam_turbine_calc()["high_steam_turbine_params"], self.pump_calc()["params_operation"])

    hrsg_mass_flows = self.hrsg.get_mass_flow(self.input, hrsg_params, heat_suplied_hrsg)

    return {
      "heat_suplied_hrsg": heat_suplied_hrsg,
      "hrsg_mass_flows": hrsg_mass_flows
    }
  
  def steam_turbine_calc(self):
    high_steam_turbine_params = self.high_steam_turbine.get_params_operation(self.input, self.saturation_parameters, self.entropy, self.enthalpy, self.secant_method)
    return {
      "high_steam_turbine_params": high_steam_turbine_params
    }
  
  def condenser_calc(self):
    return
  
  def pump_calc(self):
    params_operation = self.pump.get_params_operation(self.input, self.enthalpy, self.specific_volume, self.saturation_parameters)
    return {
      "params_operation": params_operation
    }
  
  def run(self, brayton_cycle_data):
    hrsg_data = self.HRSG_calc(brayton_cycle_data)
    pump_data = self.pump_calc()
    return {
      "hrsg_data": hrsg_data,
      "pump_data": pump_data
    }