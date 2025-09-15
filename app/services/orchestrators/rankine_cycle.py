from ..thermodynamics.steam.enthalpy import Enthalpy
from ..thermodynamics.steam.entropy import Entropy
from ..thermodynamics.steam.saturation_parameters import SaturationParameters
from ..equipments.HRSG import HRSG
from ..equipments.high_steam_turbine import HighSteamTurbine

class RankineCycle:
  """Service class of all methods and calculations related to Rankine's cycle"""
  def __init__(self, input, substance_repo, icph_repo):
    self.input = input
    self.substance_repo = substance_repo
    self.icph_repo = icph_repo
    self.enthalpy = Enthalpy()
    self.entropy = Entropy()
    self.hrsg = HRSG()
    self.saturation_parameters = SaturationParameters()
    self.high_steam_turbine = HighSteamTurbine()
  
  def HRSG_calc(self):
    """Calculating operation conditions and properties of HRSG"""
    hrsg_params = self.hrsg.get_params_operation(self.enthalpy, self.entropy, self.saturation_parameters)
    return
  