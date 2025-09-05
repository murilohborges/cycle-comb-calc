class InputAir:
  """
  Service class to calculate input air's properties.
  """
  def __init__(self, input_data, substance_repository, icph_repository):
    self.input = input_data
    self.substance_repo = substance_repository
    self.icph_repo = icph_repository
  
  def fraction_molar_calc(self, flows):
    """
    Calculation of molar fractions of input air.
    """
    total_flow = sum(flows.values())

    fractions = {
        name: flow / total_flow
        for name, flow in flows.items()
      }
    return fractions
  
  def average_molar_mass_calc(self, fractions) -> float:
    """Calculating average molar mass of input air in kmol/kg"""
    db_components = self.substance_repo.get_all()
    return sum(
      fractions[name] * db_components[name]["molar_mass"]
      for name in fractions
    )
  
  def icph_params_calc(self, fractions):
    """Calculating ICPH params of input air"""
    weighted_params = {"param_A": 0, "param_B": 0, "param_C": 0, "param_D": 0}
    db_components = self.substance_repo.get_all()

    for substance, fraction in fractions.items():
      substance_id = db_components[substance]["id"]
      icph_params = self.icph_repo.get_by_substance_id(substance_id)

      if not icph_params:
        raise ValueError(f"ICPH params not found for substance_id={substance_id}")

      for key in weighted_params:
        weighted_params[key] += fraction * icph_params[key]

    return weighted_params
  
  def input_air_data_calc(self, oxygen_stoichiometric, absolute_humidity):
    """Calculation of properties of input air"""
    # Calculation dry air properties
    nitrogen_stoichiometric = oxygen_stoichiometric * (79/21)
    dry_air_molar_flow = {
      "oxygen": oxygen_stoichiometric,
      "nitrogen": nitrogen_stoichiometric
    }
    dry_air_fractions = self.fraction_molar_calc(dry_air_molar_flow)
    dry_air_molar_mass = self.average_molar_mass_calc(dry_air_fractions)

    # Get water mass molar in repository
    db_components = self.substance_repo.get_all()

    # Calculating molar flow of water in atmospheric
    water_input_air = sum(dry_air_molar_flow.values())*dry_air_molar_mass*absolute_humidity*(1/db_components["water"]["molar_mass"])*(1+(self.input.percent_excess_air/100))

    air_molar_flow = {
      "oxygen": oxygen_stoichiometric * (1+(self.input.percent_excess_air/100)),
      "nitrogen": nitrogen_stoichiometric * (1+(self.input.percent_excess_air/100)),
      "water": water_input_air
    }

    # Calculating molar fractions, molar mass and mass flow of input air
    air_fractions = self.fraction_molar_calc(air_molar_flow)
    air_molar_mass = self.average_molar_mass_calc(air_fractions)
    air_mass_flow = sum(air_molar_flow.values())*air_molar_mass

    # Calculating icph params of input air
    air_icph_params = self.icph_params_calc(air_fractions)

    input_air_data = {
      "molar_flow": air_molar_flow,
      "fractions": air_fractions,
      "molar_mass": air_molar_mass,
      "mass_flow": air_mass_flow,
      "icph_params": air_icph_params
    }
    return input_air_data