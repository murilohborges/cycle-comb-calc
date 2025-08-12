from sqlmodel import select
from ..database.models import Substance

class GasFuel:
  def __init__(self, input, db):
    self.input = input
    self.db = db

  # Calculation of PCI of Gas Fuel
  def LHV_fuel_calc(self):
    # Validate sum of percents of components in gas fuel
    fractions = [
        (fraction / 100)
        for name, fraction in vars(self.input).items()
        if name.endswith("_molar_fraction_fuel")
      ]
        
    sum_percent_components = sum(fractions)
    
    if sum_percent_components != 1.0:
      raise ValueError(f"Percent invalid: sum = {sum_percent_components}%")
    
    # Getting lhv's and molar mass values of each component
    statement = select(Substance.lower_calorific_value, Substance.molar_mass)
    results = self.db.exec(statement).all()

    # Calculating LHV fuel in Joules/mol
    LHV_fuel_joule_per_mol = sum(frac * lhv for frac, (lhv, _) in zip(fractions, results))

    # Calculating average molar mass of fuel in kmol/kg
    average_molar_mass_fuel = sum(frac * molar_mass for frac, (_, molar_mass) in zip(fractions, results))

    # Calculating LHV fuel in kJ/kg
    LHV_fuel = LHV_fuel_joule_per_mol/average_molar_mass_fuel

    return LHV_fuel