import pytest
from unittest.mock import MagicMock
from app.services.orchestrators.brayton_cycle import BraytonCycle

@pytest.fixture
def mock_dependencies():
  # Creating mocks for external dependencies
  mock_input = MagicMock()
  mock_substance_repo = MagicMock()
  mock_icph_repo = MagicMock()
  return mock_input, mock_substance_repo, mock_icph_repo


def test_brayton_cycle_run_normal(mock_dependencies, monkeypatch):
  """Test brayton cycle calculation with valid data."""
  mock_input, mock_substance_repo, mock_icph_repo = mock_dependencies

  # Mock of auxiliary classes instantiated in the constructor
  mock_gas_fuel = MagicMock()
  mock_gas_fuel.LHV_fuel_calc.return_value = 45.2

  mock_icph = MagicMock()
  mock_reactions = MagicMock()
  mock_input_air = MagicMock()
  mock_combustion_gas = MagicMock()
  mock_humidity = MagicMock()
  mock_saturation_parameters = MagicMock()
  mock_gas_turbine_config = MagicMock()

  mock_gas_turbine = MagicMock()
  mock_gas_turbine.fuel_sensible_heat_calc.return_value = 12.5
  mock_gas_turbine.net_power_GT_calculation.return_value = 15000
  mock_gas_turbine.input_air_properties.return_value = {"temperature": 300}
  mock_gas_turbine.combustion_gas_properties.return_value = {"pressure": 101325}
  mock_gas_turbine.exhaustion_gas_temp.return_value = 750

  # Patching to replace real classes with mocks
  monkeypatch.setattr("app.services.orchestrators.brayton_cycle.GasFuel", lambda *a, **kw: mock_gas_fuel)
  monkeypatch.setattr("app.services.orchestrators.brayton_cycle.ICPH", lambda *a, **kw: mock_icph)
  monkeypatch.setattr("app.services.orchestrators.brayton_cycle.Reactions", lambda *a, **kw: mock_reactions)
  monkeypatch.setattr("app.services.orchestrators.brayton_cycle.InputAir", lambda *a, **kw: mock_input_air)
  monkeypatch.setattr("app.services.orchestrators.brayton_cycle.CombustionGas", lambda *a, **kw: mock_combustion_gas)
  monkeypatch.setattr("app.services.orchestrators.brayton_cycle.Humidity", lambda *a, **kw: mock_humidity)
  monkeypatch.setattr("app.services.orchestrators.brayton_cycle.SaturationParameters", lambda *a, **kw: mock_saturation_parameters)
  monkeypatch.setattr("app.services.orchestrators.brayton_cycle.GasTurbineConfig", lambda *a, **kw: mock_gas_turbine_config)
  monkeypatch.setattr("app.services.orchestrators.brayton_cycle.GasTurbine", lambda *a, **kw: mock_gas_turbine)

  # Instantiate the class
  cycle = BraytonCycle(mock_input, mock_substance_repo, mock_icph_repo)

  # Execute the method
  result = cycle.run()

  # Validation
  assert result["LHV_fuel"] == 45.2
  assert result["fuel_sensible_heat"] == 12.5
  assert result["net_power"] == 15000
  assert result["input_air"]["temperature"] == 300
  assert result["combustion_gas"]["pressure"] == 101325
  assert result["exhaustion_temp"] == 750

  # Checks if the main mocks were actually called
  mock_gas_fuel.LHV_fuel_calc.assert_called_once()
  mock_gas_turbine.net_power_GT_calculation.assert_called_once()

def test_brayton_cycle_run_with_error(mock_dependencies, monkeypatch):
  """Test brayton cycle calculation with invalid data."""
  """Erro in LHV calculation"""
  mock_input, mock_substance_repo, mock_icph_repo = mock_dependencies

  # Creates mocks of dependencies
  mock_gas_fuel = MagicMock()
  mock_gas_turbine = MagicMock()

  # Simulates an error in obtaining the fuel's LHV
  mock_gas_fuel.LHV_fuel_calc.side_effect = ValueError("Error in LHV calculation")

  # Mock other dependencies that do not influence the error
  mock_icph = MagicMock()
  mock_reactions = MagicMock()
  mock_input_air = MagicMock()
  mock_combustion_gas = MagicMock()
  mock_humidity = MagicMock()
  mock_saturation_parameters = MagicMock()
  mock_gas_turbine_config = MagicMock()

  # Patching the classes used within Brayton Cycle
  monkeypatch.setattr("app.services.orchestrators.brayton_cycle.GasFuel", lambda *a, **kw: mock_gas_fuel)
  monkeypatch.setattr("app.services.orchestrators.brayton_cycle.ICPH", lambda *a, **kw: mock_icph)
  monkeypatch.setattr("app.services.orchestrators.brayton_cycle.Reactions", lambda *a, **kw: mock_reactions)
  monkeypatch.setattr("app.services.orchestrators.brayton_cycle.InputAir", lambda *a, **kw: mock_input_air)
  monkeypatch.setattr("app.services.orchestrators.brayton_cycle.CombustionGas", lambda *a, **kw: mock_combustion_gas)
  monkeypatch.setattr("app.services.orchestrators.brayton_cycle.Humidity", lambda *a, **kw: mock_humidity)
  monkeypatch.setattr("app.services.orchestrators.brayton_cycle.SaturationParameters", lambda *a, **kw: mock_saturation_parameters)
  monkeypatch.setattr("app.services.orchestrators.brayton_cycle.GasTurbineConfig", lambda *a, **kw: mock_gas_turbine_config)
  monkeypatch.setattr("app.services.orchestrators.brayton_cycle.GasTurbine", lambda *a, **kw: mock_gas_turbine)

  # Instantiate the class
  cycle = BraytonCycle(mock_input, mock_substance_repo, mock_icph_repo)

  # Checks if the error is propagated correctly
  with pytest.raises(ValueError, match="Error in LHV calculation"):
    cycle.run()