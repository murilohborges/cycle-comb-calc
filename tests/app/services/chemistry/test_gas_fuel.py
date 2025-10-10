import pytest
from app.services.chemistry.gas_fuel import GasFuel
from app.utils.errors import LogicConstraintError, ThermodynamicError, DataValidationError

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
      "methane":{'id': 2, 'molar_mass': 0.014, 'lower_calorific_value': 45000},
      "nitrogen":{'id': 3, 'molar_mass': 0.028, 'lower_calorific_value': 0},
      "water":{'id': 4, 'molar_mass': 0.018, 'lower_calorific_value': 0}
    }
  def get_all(self):
    return self.results
  
class MockInvalidSubstanceRepository:
  def get_all(self):
    return 0

class MockICPHRepository:
  def __init__(self):
    self.results = [
        {"param_A": 1.0, "param_B": 2.0, "param_C": 3.0, "param_D": 4.0},
        {"param_A": 2.0, "param_B": 4.0, "param_C": 6.0, "param_D": 8.0},
        {"param_A": 2.5, "param_B": 3.0, "param_C": 9.0, "param_D": 0.0},
        {"param_A": 2.7, "param_B": 5.0, "param_C": 0.0, "param_D": 10.0}
      ]
  def get_by_substance_id(self, substance_id):
    return self.results[(substance_id - 1)]

class MockInvalidICPHRepository:
  def __init__(self):
    self.results = 0
  def get_by_substance_id(self, substance_id):
    return 0

class TestGasFuel:

  def test_validate_fractions(self, fractions_case, mock_input_factory):
    """
    Testing the validation of fractions.
    - If sum = 1.0 -> it shouldn't throw error
    - If sum != 1.0 -> it should throw error
    """
    #Creates the MockInput object from the fractions_case fixture dictionary
    mock_input_obj = mock_input_factory(**fractions_case)

    #Mocks repositories (not used in this test)
    substance_repo_mock = MockSubstanceRepository()
    icph_repo_mock = MockICPHRepository()

    gas_fuel = GasFuel(mock_input_obj, substance_repo_mock, icph_repo_mock)

    total = sum(fractions_case.values())
    if total == 100:
      # correct sum (valid)
      gas_fuel._validate_fractions()
    else:
      # incorrect sum (invalid)
      with pytest.raises(LogicConstraintError):
        gas_fuel._validate_fractions()
  
  def test_average_molar_mass(self, mock_input_factory):
    """Testing avarege molar mass calculation"""
    fractions = {"hydrogen_molar_fraction_fuel": 30, "methane_molar_fraction_fuel": 70}
    mock_input = mock_input_factory(**fractions)
    substance_repo_mock = MockSubstanceRepository()
    icph_repo_mock = MockICPHRepository()
    
    gas_fuel = GasFuel(mock_input, substance_repo_mock, icph_repo_mock)
    result = gas_fuel.average_molar_mass_calc()

    # Checks if the result is calculated correctly
    expected_molar_mass = (0.3 * 0.016) + (0.7 * 0.014)

    assert result == pytest.approx(expected_molar_mass)
  
  def test_average_molar_mass_invalid_data(self, mock_input_factory):
    """Testing avarege molar mass calculation without components data"""
    fractions = {"hydrogen_molar_fraction_fuel": 30, "methane_molar_fraction_fuel": 70}
    mock_input = mock_input_factory(**fractions)
    substance_repo_mock = MockInvalidSubstanceRepository()
    icph_repom_mock = MockInvalidICPHRepository()

    gas_fuel = GasFuel(mock_input, substance_repo_mock, icph_repom_mock)

    # Checks if Validation Error is raised
    with pytest.raises(DataValidationError):
      result = gas_fuel.average_molar_mass_calc()


  def test_lhv_calculation_with_valid_data(self, mock_input_factory):
    """
    Test LHV calculation with valid data.
    """
    fractions = {"hydrogen_molar_fraction_fuel": 30, "methane_molar_fraction_fuel": 70}
    mock_input = mock_input_factory(**fractions)
    substance_mock_repository = MockSubstanceRepository()
    icph_mock_repository = MockICPHRepository()

    service = GasFuel(mock_input, substance_mock_repository, icph_mock_repository)
    result = service.LHV_fuel_calc()

    # Checks if the result is calculated correctly
    expected_lhv_joule_per_mol = (0.3 * 50000) + (0.7 * 45000)
    expected_molar_mass = (0.3 * 0.016) + (0.7 * 0.014)
    expected_lhv = expected_lhv_joule_per_mol / expected_molar_mass

    assert result == pytest.approx(expected_lhv, rel=1e-2)
  
  def test_lhv_calculation_with_invalid_data(self, mock_input_factory):
    """
    Test LHV calculation with invalid data, with only inerts in composition.
    """
    fractions = {"nitrogen_molar_fraction_fuel": 80, "water_molar_fraction_fuel": 20}
    mock_input = mock_input_factory(**fractions)
    substance_mock_repository = MockSubstanceRepository()
    icph_mock_repository = MockICPHRepository()

    service = GasFuel(mock_input, substance_mock_repository, icph_mock_repository)

    # Checks if the Validation Error is raised
    with pytest.raises(ThermodynamicError):
      service.LHV_fuel_calc()
    
  
  def test_icph_params_calc(self, mock_input_factory):
    """
    Test ICPH params calculation of gas fuel with valid data.
    """
    fractions = {"hydrogen_molar_fraction_fuel": 30, "methane_molar_fraction_fuel": 70}
    mock_input = mock_input_factory(**fractions)
    substance_mock_repository = MockSubstanceRepository()
    icph_mock_repository = MockICPHRepository()

    service = GasFuel(mock_input, substance_mock_repository, icph_mock_repository)
    result = service.icph_params_calc()

    #Calculations manually the expected values
    expected_param_A = (0.3 * 1) + (0.7 * 2)
    expected_param_B = (0.3 * 2) + (0.7 * 4)
    expected_param_C = (0.3 * 3) + (0.7 * 6)
    expected_param_D = (0.3 * 4) + (0.7 * 8)
    expected_params = {
      "param_A": expected_param_A,
      "param_B": expected_param_B,
      "param_C": expected_param_C,
      "param_D": expected_param_D
    }

    #Checks if the result is calculated correctly
    assert result == pytest.approx(expected_params, rel=1e-2)