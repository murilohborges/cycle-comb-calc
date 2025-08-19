import pytest
from app.services.chemistry.gas_fuel import GasFuel
from tests.conftest import MockDB


# Fixture parametrizada para frações de combustível
@pytest.fixture(
      params=[
        # sum = 1.0 (valid)
        {"hydrogen_molar_fraction_fuel": 50, "methane_molar_fraction_fuel": 50},
        # sum < 1.0 (invalid)
        {"hydrogen_molar_fraction_fuel": 40, "methane_molar_fraction_fuel": 50},
        # sum > 1.0 (invalid)
        {"hydrogen_molar_fraction_fuel": 60, "methane_molar_fraction_fuel": 50},
      ],
      ids=["sum_100", "sum_lt_100", "sum_gt_100"]
  )
def fractions_case(request):
    """
    Parameterized fixture to test different sums of fractions.
    """
    return request.param

# Mock for SubstanceRepository
class MockSubstanceRepository:
    def __init__(self):
        self.results = {
          "hydrogen":{'id': 1, 'molar_mass': 0.016, 'lower_calorific_value': 50000},
          "methane":{'id': 2, 'molar_mass': 0.014, 'lower_calorific_value': 45000}
        }
    def get_all(self):
        return self.results

class TestGasFuel:

  def test_validate_fractions(self, fractions_case, mock_input_factory):
    """
    Testing the validation of fractions.
    - If sum = 1.0 -> it shouldn't throw error
    - If sum != 1.0 -> it should throw error
    """
    #Creates the MockInput object from the fractions_case fixture dictionary
    mock_input_obj = mock_input_factory(**fractions_case)

    #Mock repository (not used in this test)
    repository_mock = MockSubstanceRepository()

    gas_fuel = GasFuel(mock_input_obj, repository_mock)

    total = sum(fractions_case.values())
    if total == 100:
      # correct sum (valid)
      gas_fuel._validate_fractions()
    else:
      # incorrect sum (invalid)
      with pytest.raises(ValueError):
        gas_fuel._validate_fractions()
  
  def test_average_molar_mass(self, mock_input_factory):
    """Testing avarege molar mass calculation"""
    fractions = {"hydrogen_molar_fraction_fuel": 30, "methane_molar_fraction_fuel": 70}
    mock_input = mock_input_factory(**fractions)
    mock_repository = MockSubstanceRepository()
    
    gas_fuel = GasFuel(mock_input, mock_repository)
    result = gas_fuel.average_molar_mass_calc()

    # Checks if the result is calculated correctly
    expected_molar_mass = (0.3 * 0.016) + (0.7 * 0.014)

    assert result == pytest.approx(expected_molar_mass)

  def test_lhv_calculation_with_valid_data(self, mock_input_factory):
    """
    Test LHV calculation with valid data.
    """
    fractions = {"hydrogen_molar_fraction_fuel": 30, "methane_molar_fraction_fuel": 70}
    mock_input = mock_input_factory(**fractions)
    mock_repository = MockSubstanceRepository()

    service = GasFuel(mock_input, mock_repository)
    result = service.LHV_fuel_calc()

    # Checks if the result is calculated correctly
    expected_lhv_joule_per_mol = (0.3 * 50000) + (0.7 * 45000)
    expected_molar_mass = (0.3 * 0.016) + (0.7 * 0.014)
    expected_lhv = expected_lhv_joule_per_mol / expected_molar_mass

    assert result == pytest.approx(expected_lhv, rel=1e-2)