class InputAir:
  """
  Service class to calculate input air's properties.
  """
  def __init__(self, input_data, substance_repository):
    self.input = input_data
    self.substance_repo = substance_repository
  
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
  
  def molar_flow_calc(self, oxygen_stoichiometric, absolute_humidity):
    """
    Calculation of molar flow of input air.
    """
    nitrogen_stoichiometric = oxygen_stoichiometric * (79/21)
    dry_air_molar_flow = {
      "oxygen": oxygen_stoichiometric,
      "nitrogen": nitrogen_stoichiometric
    }
    dry_air_fractions = self.fraction_molar_calc(dry_air_molar_flow)
    dry_air_molar_mass = self.average_molar_mass_calc(dry_air_fractions)

    water_input_air = sum(dry_air_molar_flow.values())*dry_air_molar_mass
    print(water_input_air)

    return
  
  def icph_params_calc():
    return