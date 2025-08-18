class GasFuel:
  def __init__(self, input, repository):
    self.input = input
    self.repository = repository
    self.fractions = [
        (fraction / 100)
        for name, fraction in vars(self.input).items()
        if name.endswith("_molar_fraction_fuel")
      ]

  # Calculation of PCI of Gas Fuel
  def LHV_fuel_calc(self):
    # Validate sum of percents of components in gas fuel
    sum_percent_components = sum(self.fractions)
    
    if sum_percent_components != 1.0:
      raise ValueError(f"Percent invalid: sum = {sum_percent_components}%")
    
    # Getting lhv's and molar mass values of each component
    results = self.repository.get_all()

    # Calculating LHV fuel in Joules/mol
    LHV_fuel_joule_per_mol = sum(frac * lhv for frac, (lhv, _) in zip(self.fractions, results))

    # Calculating average molar mass of fuel in kmol/kg
    average_molar_mass_fuel = sum(frac * molar_mass for frac, (_, molar_mass) in zip(self.fractions, results))

    # Calculating LHV fuel in kJ/kg
    LHV_fuel = round(LHV_fuel_joule_per_mol/average_molar_mass_fuel, 2)

    return LHV_fuel