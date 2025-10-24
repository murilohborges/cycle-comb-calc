import pytest
from unittest.mock import MagicMock
from app.services.cycles_analysis.cycles_performances import CyclesPerformances
from app.utils.errors import ThermodynamicError

@pytest.fixture
def mock_input():
  mock = MagicMock()
  mock.fuel_mass_flow = 10  # kg/s, arbitrary value
  return mock

def test_cycles_effiencies_calc_normal(mock_input):
  """Test brayton cycle calculation with valid data."""
  service = CyclesPerformances()

  # Fictitious input data
  net_power_gas_turbine = 100_000     # W
  LHV_fuel = 500_000_000                 # J/kg
  fuel_sensible_heat = 5_000_000        # J/kg
  rankine_cycle_data = {"net_power_steam_turbine": 200_000, "consumed_power": 5_000}

  result = service.cycles_effiencies_calc(
    mock_input,
    net_power_gas_turbine,
    LHV_fuel,
    fuel_sensible_heat,
    rankine_cycle_data
  )

  # Basic validations
  assert result["gross_cycle_combined_efficiency"] < 100
  assert result["net_cycle_combined_efficiency"] < 100
  assert round(result["gross_cycle_combined_efficiency"], 2) == 21.39
  assert round(result["net_cycle_combined_efficiency"], 2) == 21.03


def test_cycles_effiencies_calc_efficiency_error(mock_input):
  """Test brayton cycle calculation with invalid data."""
  service = CyclesPerformances()

  # Absurd values ​​that generate efficiency > 100%
  net_power_gas_turbine = 1_000_000_000    # W, Absurd value
  LHV_fuel = 10_000                         # J/kg, very low value
  fuel_sensible_heat = 0
  rankine_cycle_data = {"net_power_steam_turbine": 500_000_000, "consumed_power": 100_000_000}

  with pytest.raises(ThermodynamicError, match="efficiency"):
    service.cycles_effiencies_calc(
      mock_input,
      net_power_gas_turbine,
      LHV_fuel,
      fuel_sensible_heat,
      rankine_cycle_data
    )
