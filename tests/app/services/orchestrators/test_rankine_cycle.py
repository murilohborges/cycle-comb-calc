import pytest
from unittest.mock import MagicMock
from app.services.orchestrators.rankine_cycle import RankineCycle
from app.utils.errors import ThermodynamicError

@pytest.fixture
def mock_dependencies():
  mock_input = MagicMock()
  mock_substance_repo = MagicMock()
  mock_icph_repo = MagicMock()
  mock_heat_suplier_cycle = {
    "combustion_gas": MagicMock(),
    "exhaustion_temp": 800
  }
  return mock_input, mock_substance_repo, mock_icph_repo, mock_heat_suplier_cycle


def test_rankine_cycle_run_normal(mock_dependencies, monkeypatch):
  """Test brayton cycle calculation with valid data."""
  mock_input, mock_substance_repo, mock_icph_repo, mock_heat_suplier_cycle = mock_dependencies

  # Mocks for all equipment
  mock_hrsg = MagicMock()
  mock_high_turbine = MagicMock()
  mock_medium_turbine = MagicMock()
  mock_low_turbine = MagicMock()
  mock_pump = MagicMock()
  mock_condenser = MagicMock()
  mock_saturation = MagicMock()

  # Fictitious return data
  mock_high_turbine.get_params_operation.return_value = {"delta_enthalpy_real": 5000}
  mock_medium_turbine.get_params_operation.return_value = {"delta_enthalpy_real": 3000}
  mock_low_turbine.get_params_operation.return_value = {"delta_enthalpy_real": 2000}
  mock_hrsg.heat_supplied_calc.return_value = 10000
  mock_hrsg.get_params_operation.return_value = {"param": 1}
  mock_hrsg.get_mass_flow.return_value = {
    "high_steam": 3600,
    "medium_steam": 1800,
    "total_steam_generated": 5400
  }
  mock_pump.get_params_operation.return_value = {"delta_specific_enthalpy": 50}
  mock_condenser.get_params_operation.return_value = {"saturated_water_mass_flow": 7200}
  mock_saturation.saturation_temperature.return_value = 50
  mock_input.chimney_gas_temperature = 100

  # Patching RankineCycle classes
  monkeypatch.setattr("app.services.orchestrators.rankine_cycle.HRSG", lambda *a, **kw: mock_hrsg)
  monkeypatch.setattr("app.services.orchestrators.rankine_cycle.HighSteamTurbine", lambda *a, **kw: mock_high_turbine)
  monkeypatch.setattr("app.services.orchestrators.rankine_cycle.MediumSteamTurbine", lambda *a, **kw: mock_medium_turbine)
  monkeypatch.setattr("app.services.orchestrators.rankine_cycle.LowSteamTurbine", lambda *a, **kw: mock_low_turbine)
  monkeypatch.setattr("app.services.orchestrators.rankine_cycle.Pump", lambda *a, **kw: mock_pump)
  monkeypatch.setattr("app.services.orchestrators.rankine_cycle.Condenser", lambda *a, **kw: mock_condenser)
  monkeypatch.setattr("app.services.orchestrators.rankine_cycle.SaturationParameters", lambda *a, **kw: mock_saturation)

  cycle = RankineCycle(mock_input, mock_substance_repo, mock_icph_repo, mock_heat_suplier_cycle)
  result = cycle.run()

  # Basic result verification
  assert result["condenser_data"] == {"saturated_water_mass_flow": 7200}
  assert result["pump_data"]["params_operation"] == {"delta_specific_enthalpy": 50}
  assert result["hrsg_data"]["heat_suplied_hrsg"] == 10000


def test_rankine_cycle_chimney_temp_error(mock_dependencies, monkeypatch):
  """Test brayton cycle calculation with invalid data."""
  """The chimney temperature is lower than that of the condenser"""
  mock_input, mock_substance_repo, mock_icph_repo, mock_heat_suplier_cycle = mock_dependencies

  mock_hrsg = MagicMock()
  mock_high_turbine = MagicMock()
  mock_medium_turbine = MagicMock()
  mock_low_turbine = MagicMock()
  mock_pump = MagicMock()
  mock_condenser = MagicMock()
  mock_saturation = MagicMock()

  # All methods return valid data
  mock_high_turbine.get_params_operation.return_value = {"delta_enthalpy_real": 5000}
  mock_medium_turbine.get_params_operation.return_value = {"delta_enthalpy_real": 3000}
  mock_low_turbine.get_params_operation.return_value = {"delta_enthalpy_real": 2000}
  mock_hrsg.heat_supplied_calc.return_value = 10000
  mock_hrsg.get_params_operation.return_value = {"param": 1}
  mock_hrsg.get_mass_flow.return_value = {"high_steam": 3600, "medium_steam": 1800, "total_steam_generated": 5400}
  mock_pump.get_params_operation.return_value = {"delta_specific_enthalpy": 50}
  mock_condenser.get_params_operation.return_value = {"saturated_water_mass_flow": 7200}

  # Condition that will generate thermodynamic error
  mock_input.chimney_gas_temperature = 40  # smaller than the condenser
  mock_saturation.saturation_temperature.return_value = 50

  # Patching the classes
  monkeypatch.setattr("app.services.orchestrators.rankine_cycle.HRSG", lambda *a, **kw: mock_hrsg)
  monkeypatch.setattr("app.services.orchestrators.rankine_cycle.HighSteamTurbine", lambda *a, **kw: mock_high_turbine)
  monkeypatch.setattr("app.services.orchestrators.rankine_cycle.MediumSteamTurbine", lambda *a, **kw: mock_medium_turbine)
  monkeypatch.setattr("app.services.orchestrators.rankine_cycle.LowSteamTurbine", lambda *a, **kw: mock_low_turbine)
  monkeypatch.setattr("app.services.orchestrators.rankine_cycle.Pump", lambda *a, **kw: mock_pump)
  monkeypatch.setattr("app.services.orchestrators.rankine_cycle.Condenser", lambda *a, **kw: mock_condenser)
  monkeypatch.setattr("app.services.orchestrators.rankine_cycle.SaturationParameters", lambda *a, **kw: mock_saturation)

  cycle = RankineCycle(mock_input, mock_substance_repo, mock_icph_repo, mock_heat_suplier_cycle)

  # ThermodynamicError is expected to be raised
  with pytest.raises(ThermodynamicError, match="chimney temperature is less than the operating condenser temperature"):
    cycle.run()
