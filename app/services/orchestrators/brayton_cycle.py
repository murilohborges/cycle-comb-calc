from ..thermodynamics.heat.icph import ICPH
from ..chemistry.reactions import Reactions
from ..chemistry.input_air import InputAir
from ..chemistry.gas_fuel import GasFuel
from ..chemistry.combustion_gas import CombustionGas
from ..thermodynamics.psychrometry.humidity import Humidity
from ..thermodynamics.steam.saturation_parameters import SaturationParameters
from ..equipments.gas_turbine import GasTurbine
from ..configs.gas_turbine_config import GasTurbineConfig

class BraytonCycle:
  """Service class of all methods and calculations related to Brayton's cycle"""
  def __init__(self, input, substance_repo, icph_repo):
    self.input = input
    self.substance_repo = substance_repo
    self.icph_repo = icph_repo

    # Instantiating auxiliary services
    self.gas_fuel = GasFuel(self.input, self.substance_repo, self.icph_repo)
    self.icph = ICPH()
    self.reactions = Reactions(self.input, self.gas_fuel.fractions, self.gas_fuel.average_molar_mass_calc(), self.substance_repo)
    self.input_air = InputAir(self.input, self.substance_repo, self.icph_repo)
    self.combustion_gas = CombustionGas(self.input, self.substance_repo, self.icph_repo)
    self.humidity = Humidity()
    self.saturation_parameters = SaturationParameters()

    # Assembling the turbine configuration
    config = GasTurbineConfig(
      input=self.input,
      gas_fuel=self.gas_fuel,
      icph=self.icph,
      substance_repo=self.substance_repo,
      icph_repo=self.icph_repo,
      reactions=self.reactions,
      combustion_gas=self.combustion_gas,
      input_air=self.input_air,
      humidity=self.humidity,
      saturation_parameters=self.saturation_parameters
    )

    # Instantiating the turbine with the configuration already packaged
    self.gas_turbine = GasTurbine(config)

  def run(self):
    return {
      "LHV_fuel": self.gas_fuel.LHV_fuel_calc(),
      "net_power": self.gas_turbine.net_power_GT_calculation(),
      "input_air": self.gas_turbine.input_air_properties(),
      "combustion_gas": self.gas_turbine.combustion_gas_properties(),
      "exhaustion_temp": self.gas_turbine.exhaustion_gas_temp()
    }