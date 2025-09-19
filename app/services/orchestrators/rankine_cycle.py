from ..thermodynamics.steam.enthalpy import Enthalpy
from ..thermodynamics.steam.entropy import Entropy
from ..thermodynamics.steam.specific_volume import SpecificVolume
from ..thermodynamics.steam.saturation_parameters import SaturationParameters
from ..thermodynamics.heat.icph import ICPH
from ..equipments.HRSG import HRSG
from ..equipments.high_steam_turbine import HighSteamTurbine
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
    self.secant_method = SecantMethod()
  
  def HRSG_calc(self, brayton_cycle_data):
    """Calculating operation conditions and properties of HRSG"""
    heat_suplied_hrsg = self.hrsg.heat_supplied_calc(self.input, brayton_cycle_data["combustion_gas"], brayton_cycle_data["exhaustion_temp"], self.icph)
    high_steam_turbine_params = self.high_steam_turbine.get_params_operation(self.input, self.saturation_parameters, self.entropy, self.enthalpy, self.secant_method)
    return
  
  def steam_turbine_calc(self):
    return
  
  def condenser_calc(self):
    return
  
  def pump_calc(self):
    return
  
  def run(self, brayton_cycle_data):
    hrsg_data = self.HRSG_calc(brayton_cycle_data)
    return