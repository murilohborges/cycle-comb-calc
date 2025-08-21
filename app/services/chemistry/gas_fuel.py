class GasFuel:
  """
  Service class intended for calculating fuel properties
  """
  def __init__(self, input, substance_repo, icph_repo):
    self.input = input
    self.substance_repo = substance_repo
    self.icph_repo = icph_repo

    # Creating a dict with fraction of components indexed by name
    self.fractions = {
        name.replace("_molar_fraction_fuel", ""): (fraction / 100)
        for name, fraction in vars(self.input).items()
        if name.endswith("_molar_fraction_fuel")
      }
    
  def _validate_fractions(self):
    """Validate sum of percents of components in gas fuel"""
    sum_percent_components = sum(self.fractions.values())
    if not (0.999 <= sum_percent_components <= 1.001):  # tolerância
      raise ValueError(f"Percent invalid: sum = {sum_percent_components*100:.2f}%")

  def average_molar_mass_calc(self) -> float:
    """Calculating average molar mass of fuel in kmol/kg"""
    db_components = self.substance_repo.get_all()
    return sum(
      self.fractions[name] * db_components[name]["molar_mass"]
      for name in self.fractions
    )

  def LHV_fuel_calc(self) -> float:
    """Calculation of PCI of Gas Fuel"""
    # Getting lhv's and molar mass values of each component
    self._validate_fractions()
    db_components = self.substance_repo.get_all()

    # Calculating LHV fuel in Joules/mol
    LHV_fuel_joule_per_mol = sum(
      self.fractions[name] * db_components[name]["lower_calorific_value"] 
      for name in self.fractions
    )

    # Calling average molar mass of fuel in kmol/kg
    avg_molar_mass = self.average_molar_mass_calc()

    # Calculating LHV fuel in kJ/kg
    LHV_fuel = round(LHV_fuel_joule_per_mol/avg_molar_mass, 2)

    return LHV_fuel

  def icph_params_calc(self):
    """Calculation of ICPH params of Gas Fuel"""
    weighted_params = {"param_A": 0, "param_B": 0, "param_C": 0, "param_D": 0}
    db_components = self.substance_repo.get_all()

    for substance, fraction in self.fractions.items():
      substance_id = db_components[substance]["id"]
      icph_params = self.icph_repo.get_by_substance_id(substance_id)

      if not icph_params:
        raise ValueError(f"ICPH params not found for substance_id={substance_id}")

      for key in weighted_params:
        weighted_params[key] += fraction * icph_params[key]

    return weighted_params