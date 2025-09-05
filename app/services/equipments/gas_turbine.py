from ..thermodynamics.heat.icph import ICPH
from ..chemistry.reactions import Reactions
from ..chemistry.input_air import InputAir
from ..chemistry.combustion_gas import CombustionGas
from ..thermodynamics.psychrometry.humidity import Humidity
from ..thermodynamics.steam.saturation_parameters import SaturationParameters

class GasTurbine:
  def __init__(self, input, gas_fuel, substance_repo, icph_repo):
    self.input = input
    self.gas_fuel = gas_fuel
    self.icph = ICPH()
    self.substance_repo = substance_repo
    self.icph_repo = icph_repo
    self.reactions = Reactions(self.input, self.gas_fuel.fractions, self.gas_fuel.average_molar_mass_calc(), self.substance_repo)
    self.input_air = InputAir(self.input, substance_repo, icph_repo)
    self.combustion_gas = CombustionGas(self.input, substance_repo, icph_repo)
    self.humidity = Humidity()
    self.saturation_parameters = SaturationParameters()
  
  def net_power_GT_calculation(self):
    """
    Calculation of Net Power of Gas Turbine
    """
    fuel_mass_flow = self.input.fuel_mass_flow
    heat_rate = 3600/(self.input.gas_turbine_efficiency/100)
    LHV_fuel = self.gas_fuel.LHV_fuel_calc()
    icph_params_gas_fuel = self.gas_fuel.icph_params_calc()
    molar_mass_gas_fuel = self.gas_fuel.average_molar_mass_calc()
    heat_fuel_input = self.icph.icph_calc_heat(icph_params_gas_fuel, molar_mass_gas_fuel, self.input.fuel_input_temperature, 25)
    net_power_GT = (fuel_mass_flow * (LHV_fuel + abs(heat_fuel_input))) / heat_rate
    return net_power_GT
  
  def input_air_properties(self):
    reaction_stoichiometric = self.reactions.molar_flow_stoichiometric_calc()
    oxygen_stoichiometric = reaction_stoichiometric['oxygen_stoichiometric']
    saturation_pressure = self.saturation_parameters.saturation_pressure(self.input.local_temperature)
    absolute_humidity = self.humidity.absolute_humidity_calc(saturation_pressure, self.input.local_atmospheric_pressure, self.input.relative_humidity)
    input_air_properties = self.input_air.input_air_data_calc(oxygen_stoichiometric, absolute_humidity)
    return input_air_properties
  
  def combustion_gas_properties(self):
    reaction_stoichiometric = self.reactions.molar_flow_stoichiometric_calc()
    gas_fuel_molar_mass = self.gas_fuel.average_molar_mass_calc()
    input_air = self.input_air_properties()
    combustion_gas_properties = self.combustion_gas.combustion_gas_data_calc(reaction_stoichiometric, input_air, gas_fuel_molar_mass)

    return combustion_gas_properties
  
  def exhaustion_gas_temp():
    return
  