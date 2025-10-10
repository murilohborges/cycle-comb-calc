from app.utils.errors import DataValidationError

class CombustionGas:
  """
  Service class to calculate combustion gas properties.
  """
  def __init__(self, input_data, substance_repository, icph_repository):
    self.input = input_data
    self.substance_repo = substance_repository
    self.icph_repo = icph_repository
  
  def fraction_molar_calc(self, flows):
    """
    Calculation of molar fractions of combustion gas.
    """
    total_flow = sum(flows.values())

    fractions = {
        name: flow / total_flow
        for name, flow in flows.items()
      }
    return fractions
  
  def average_molar_mass_calc(self, fractions) -> float:
    """Calculating average molar mass of combustion gas in kmol/kg"""
    db_components = self.substance_repo.get_all()

    if not db_components:
      raise DataValidationError("Data of components not found")

    return sum(
      fractions[name] * db_components[name]["molar_mass"]
      for name in fractions
    )
  
  def icph_params_calc(self, fractions):
    """Calculating ICPH params of gas combustion"""
    weighted_params = {"param_A": 0, "param_B": 0, "param_C": 0, "param_D": 0}
    db_components = self.substance_repo.get_all()

    if not db_components:
      raise DataValidationError("Data of components not found")

    for substance, fraction in fractions.items():
      substance_id = db_components[substance]["id"]
      icph_params = self.icph_repo.get_by_substance_id(substance_id)

      if not icph_params:
        raise DataValidationError(f"ICPH params not found for substance_id={substance_id}")

      for key in weighted_params:
        weighted_params[key] += fraction * icph_params[key]

    return weighted_params
  
  def combustion_gas_data_calc(self, stoichiometric_flow, input_air, gas_fuel_molar_mass):
    """ Calculation of properties of combustion gas"""
    # Calculating water from gas fuel
    gas_fuel_molar_flow = self.input.fuel_mass_flow/gas_fuel_molar_mass
    water_gas_fuel = gas_fuel_molar_flow * (self.input.water_molar_fraction_fuel/100)

    # Calculating total water of combustion gas
    water_molar_flow = stoichiometric_flow["water_stoichiometric"] + input_air["molar_flow"]["water"] + water_gas_fuel

    # Calculating carbon dioxide from gas fuel
    carbon_dioxide_gas_fuel = gas_fuel_molar_flow * (self.input.carbon_dioxide_molar_fraction_fuel/100)

    # Calculating total carbon dioxide of combustion gas
    carbon_dioxide_molar_flow = stoichiometric_flow["carbon_dioxide_stoichiometric"] + carbon_dioxide_gas_fuel

    # Calculating total oxygen of combustion gas (excess)
    oxygen_molar_flow = input_air["molar_flow"]["oxygen"] - stoichiometric_flow["oxygen_stoichiometric"]

    # Calculating nitrogen from gas fuel
    nitrogen_gas_fuel = gas_fuel_molar_flow * (self.input.nitrogen_molar_fraction_fuel/100)

    # Calculating total nitrogen of combustion gas
    nitrogen_molar_flow = input_air["molar_flow"]["nitrogen"] + nitrogen_gas_fuel
    
    combustion_gas_molar_flow = {
      "oxygen": oxygen_molar_flow,
      "nitrogen": nitrogen_molar_flow,
      "water": water_molar_flow,
      "carbon_dioxide": carbon_dioxide_molar_flow
    }

    # Calculating combustion gas fractions
    combustion_gas_fractions = self.fraction_molar_calc(combustion_gas_molar_flow)

    # Calculating combustion gas molar mass
    combustion_gas_molar_mass = self.average_molar_mass_calc(combustion_gas_fractions)

    # Calculating combustion gas mass flow
    combustion_gas_mass_flow = sum(combustion_gas_molar_flow.values())*combustion_gas_molar_mass

    # Calculating combustion gas ICPH params
    combustion_gas_icph_params = self.icph_params_calc(combustion_gas_fractions)

    combustion_gas_data = {
      "molar_flow": combustion_gas_molar_flow,
      "fractions": combustion_gas_fractions,
      "molar_mass": combustion_gas_molar_mass,
      "mass_flow": combustion_gas_mass_flow,
      "icph_params": combustion_gas_icph_params
    }

    return combustion_gas_data