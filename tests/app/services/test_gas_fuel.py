import pytest
from app.services.chemistry.gas_fuel import GasFuel
from tests.conftest import MockDB

# ----------------------------
# Fixture parametrizada para frações de combustível
# ----------------------------

@pytest.fixture(
      params=[
        # sum = 1.0 (valid)
        {"h2_molar_fraction_fuel": 50, "ch4_molar_fraction_fuel": 50},
        # sum < 1.0 (invalid)
        {"h2_molar_fraction_fuel": 40, "ch4_molar_fraction_fuel": 50},
        # sum > 1.0 (invalid)
        {"h2_molar_fraction_fuel": 60, "ch4_molar_fraction_fuel": 50},
      ],
      ids=["sum_100", "sum_lt_100", "sum_gt_100"]
  )
def fractions_case(request):
    """
    Parameterized fixture to test different sums of fractions.
    """
    return request.param

class TestGasFuel:
  # Testing validation of fraction of componentes of fuel
  def test_fraction_sum_validation(self, mock_input_factory, fractions_case):
    """
    Tests the validity of the sum of fractions.
    Scenarios: sum == 100%, <100%, >100%.
    """
    mock_db = MockDB(results=[(10.0, 2.0), (20.0, 4.0)])  # LHV e molar mass fictitious values
    mock_input = mock_input_factory(**fractions_case)

    service = GasFuel(mock_input, mock_db)

    result_sum = sum(v / 100 for v in fractions_case.values())

    if result_sum != 1.0:
        with pytest.raises(ValueError, match="Percent invalid"):
            service.LHV_fuel_calc()
    else:
        result = service.LHV_fuel_calc()
        assert isinstance(result, float)
        assert result > 0

    return
  
  def test_lhv_calculation_with_valid_data(self, mock_input_factory):
    """
    Test LHV calculation with valid data.
    """
    fractions = {"h2_molar_fraction_fuel": 30, "ch4_molar_fraction_fuel": 70}
    mock_input = mock_input_factory(**fractions)
    mock_db = MockDB(results=[(100.0, 2.0), (200.0, 4.0)])

    service = GasFuel(mock_input, mock_db)
    result = service.LHV_fuel_calc()

    # Checks if the result is calculated correctly
    expected_lhv_joule_per_mol = (0.3 * 100.0) + (0.7 * 200.0)
    expected_molar_mass = (0.3 * 2.0) + (0.7 * 4.0)
    expected_lhv = expected_lhv_joule_per_mol / expected_molar_mass

    assert pytest.approx(result) == expected_lhv