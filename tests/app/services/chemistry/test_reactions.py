import pytest
from app.services.chemistry.reactions import Reactions
from app.utils.errors import NotFoundError

# Mock for SubstanceRepository
class MockSubstanceRepository:
  def __init__(self):
    self.results = {
      "methane": {"formula": "CH4", "lower_calorific_value": 50000},
      "hydrogen": {"formula": "H2", "lower_calorific_value": 120000},
      "ethane": {"formula": "C2H6", "lower_calorific_value": 47000},
      "propane": {"formula": "C3H8", "lower_calorific_value": 46000},
      "ZeroLHV": {"formula": "CH4", "lower_calorific_value": 0}
    }
  def get_all(self):
    return self.results

class MockInvalidSubstanceRepository:
  def __init__(self):
    self.results = 0
  def get_all(self):
    return self.results


class TestReactions:
  def test_parse_formula(self):
    """Testing parse_formula() with random examples"""
    r = Reactions(None, None, None, None)
    assert r.parse_formula("CH4") == (1, 4)
    assert r.parse_formula("C2H6") == (2, 6)
    assert r.parse_formula("H2") == (0, 2)
    assert r.parse_formula("C10H22") == (10, 22)
    assert r.parse_formula("C") == (1, 0)

  def test_methane_stoichiometry(self, mock_input_factory):
    """Testing molar flows with methane pure"""
    mock_input = mock_input_factory(fuel_mass_flow=16) # g/s
    fuel_fractions = {"methane": 1.0}
    fuel_molar_mass = 16  # g/mol
    repo = MockSubstanceRepository()

    r = Reactions(mock_input, fuel_fractions, fuel_molar_mass, repo)
    result = r.molar_flow_stoichiometric_calc()

    # CH4 + 2 O2 → CO2 + 2 H2O
    assert result["oxygen_stoichiometric"] == pytest.approx(2.0)
    assert result["carbon_dioxide_stoichiometric"] == pytest.approx(1.0)
    assert result["water_stoichiometric"] == pytest.approx(2.0)

  def test_ethane_stoichiometry(self, mock_input_factory):
    """Testing molar flows with ethane pure"""
    mock_input = mock_input_factory(fuel_mass_flow=30)  # g/s
    fuel_fractions = {"ethane": 1.0}
    fuel_molar_mass = 30  # g/mol
    repo = MockSubstanceRepository()

    r = Reactions(mock_input, fuel_fractions, fuel_molar_mass, repo)
    result = r.molar_flow_stoichiometric_calc()

    # C2H6 + 3.5 O2 → 2 CO2 + 3 H2O
    assert result["oxygen_stoichiometric"] == pytest.approx(3.5)
    assert result["carbon_dioxide_stoichiometric"] == pytest.approx(2.0)
    assert result["water_stoichiometric"] == pytest.approx(3.0)

  def test_mixture_stoichiometry(self, mock_input_factory):
    """Testing molar flows with methane/ethane mixture"""
    input_data = mock_input_factory(fuel_mass_flow=46)  # kg/h
    fuel_fractions = {"methane": 0.5, "ethane": 0.5}
    fuel_molar_mass = 23  # previously value calculated
    repo = MockSubstanceRepository()

    r = Reactions(input_data, fuel_fractions, fuel_molar_mass, repo)
    result = r.molar_flow_stoichiometric_calc()

    # For approximate deterministic testing only
    assert result["oxygen_stoichiometric"] == pytest.approx(5.5)
    assert result["carbon_dioxide_stoichiometric"] == pytest.approx(3.0)
    assert result["water_stoichiometric"] == pytest.approx(5.0)

  def test_zero_lhv_ignored(self, mock_input_factory):
    """Testing molar flows with substance without lhv's values"""
    input_data = mock_input_factory(fuel_mass_flow=16)
    fuel_fractions = {"ZeroLHV": 1.0}
    fuel_molar_mass = 16
    repo = MockSubstanceRepository()

    r = Reactions(input_data, fuel_fractions, fuel_molar_mass, repo)
    result = r.molar_flow_stoichiometric_calc()

    # Should be ignored → all zero
    assert result["oxygen_stoichiometric"] == 0
    assert result["carbon_dioxide_stoichiometric"] == 0
    assert result["water_stoichiometric"] == 0

  def test_invalid_repo(self, mock_input_factory):
    """Testing molar flows with invalid data repo"""
    input_data = mock_input_factory(fuel_mass_flow=16)
    fuel_fractions = {"ZeroLHV": 1.0}
    fuel_molar_mass = 16
    repo = MockInvalidSubstanceRepository()
    r = Reactions(input_data, fuel_fractions, fuel_molar_mass, repo)

    # Checks if Error Validation is raised
    with pytest.raises(NotFoundError):
      r.molar_flow_stoichiometric_calc()
