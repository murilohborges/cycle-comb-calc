from ..thermodynamics.heat.icph import ICPH
from ..chemistry.reactions import Reactions
from ..chemistry.input_air import InputAir
from ..chemistry.combustion_gas import CombustionGas
from ..thermodynamics.psychrometry.humidity import Humidity
from ..thermodynamics.steam.saturation_parameters import SaturationParameters

class GasTurbine:
  """Service class of all methods and calculations related to gas turbine"""
  def __init__(self, config):
    self.config = config
    self.input = config.input
    self.gas_fuel = config.gas_fuel
    self.icph = config.icph
    self.substance_repo = config.substance_repo
    self.icph_repo = config.icph_repo
    self.reactions = config.reactions
    self.input_air = config.input_air
    self.combustion_gas = config.combustion_gas
    self.humidity = config.humidity
    self.saturation_parameters = config.saturation_parameters

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
    """
    Calculation of input air properties
    """
    reaction_stoichiometric = self.reactions.molar_flow_stoichiometric_calc()
    oxygen_stoichiometric = reaction_stoichiometric['oxygen_stoichiometric']
    saturation_pressure = self.saturation_parameters.saturation_pressure(self.input.local_temperature)
    absolute_humidity = self.humidity.absolute_humidity_calc(saturation_pressure, self.input.local_atmospheric_pressure, self.input.relative_humidity)
    input_air_properties = self.input_air.input_air_data_calc(oxygen_stoichiometric, absolute_humidity)
    return input_air_properties

  def combustion_gas_properties(self):
    """
    Calculation of combustion gas properties
    """
    reaction_stoichiometric = self.reactions.molar_flow_stoichiometric_calc()
    gas_fuel_molar_mass = self.gas_fuel.average_molar_mass_calc()
    input_air = self.input_air_properties()
    combustion_gas_properties = self.combustion_gas.combustion_gas_data_calc(reaction_stoichiometric, input_air, gas_fuel_molar_mass)

    return combustion_gas_properties

  def exhaustion_gas_temp(self):
    """
    Calculation of exhaustion gas temperature of gas turbine
    """
    # Getting params to the calculation
    initial_temperature = 298.15
    gas_turbine_efficiency = self.input.gas_turbine_efficiency/100
    combustion_gas = self.combustion_gas_properties()
    combustion_gas_molar_mass = combustion_gas["molar_mass"]
    input_air = self.input_air_properties()
    air_mass_flow = input_air["mass_flow"]
    fuel_mass_flow = self.input.fuel_mass_flow
    LHV_fuel = self.gas_fuel.LHV_fuel_calc()
    R = 8.314462618

    # Obtaining the sensible heat from the fuel
    icph_params_gas_fuel = self.gas_fuel.icph_params_calc()
    molar_mass_gas_fuel = self.gas_fuel.average_molar_mass_calc()
    fuel_sensible_heat = self.icph.icph_calc_heat(icph_params_gas_fuel, molar_mass_gas_fuel, self.input.fuel_input_temperature, 25)

    # Obtaining the sensible heat from the input air
    icph_params_input_air = input_air["icph_params"]
    molar_mass_input_air = input_air["molar_mass"]
    input_air_sensible_heat = self.icph.icph_calc_heat(icph_params_input_air, molar_mass_input_air, self.input.air_input_temperature, 25)

    # Getting icph_params of combustion gas
    A = combustion_gas["icph_params"]["param_A"]
    B = combustion_gas["icph_params"]["param_B"]
    C = combustion_gas["icph_params"]["param_C"]
    D = combustion_gas["icph_params"]["param_D"]

    # Defining parameters for each loop of the iteration, in order to converge to the final temperature
    tolerance = 1
    old_temperature = 1
    new_temperature = initial_temperature + 1

    # Ratio of the new iteration temperature to the initial combustion gas temperature of 25°C
    tau = new_temperature / initial_temperature

    # Calculation of heat not converted into electrical energy and supplied to the flue gases in kJ/kg
    heat_supplied = ((1 - gas_turbine_efficiency) * (fuel_mass_flow * (LHV_fuel + abs(fuel_sensible_heat)) + air_mass_flow * abs(input_air_sensible_heat))) / (combustion_gas["mass_flow"])

    # Looping
    while tolerance > 0.001:
      average_specific_heat = R * (A + (B / 2) * initial_temperature * (tau + 1) + (C / 3) * (initial_temperature ** 2) * ((tau ** 2) + tau + 1) + (D / (tau * (initial_temperature ** 2))))

      new_temperature = (heat_supplied / (average_specific_heat / combustion_gas_molar_mass)) + initial_temperature

      tolerance = abs((new_temperature - old_temperature))

      old_temperature = new_temperature

      tau = new_temperature / initial_temperature

    result = new_temperature - 273.15

    return result
