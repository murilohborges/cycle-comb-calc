import pytest
from app.services.orchestrators.full_cycles import FullCycles, FullCyclesResult

class MockInput:
  """Mock class to simulate input parameters for the cycle performance calculation."""
  def __init__(self):
    self.some_param = 1

def test_full_cycles_combined_normal(monkeypatch):
  """Test brayton cycle calculation with valid data."""

  # --- Mocks of internal dependencies ---
  mock_input = MockInput()

  brayton_mock_data = {
    "LHV_fuel": 500_000_000,
    "net_power": 100_000,
    "input_air": {"mass_flow": 20.0},
    "combustion_gas": {"mass_flow": 22.0},
    "exhaustion_temp": 450.0,
    "fuel_sensible_heat": 5_000_000
  }

  rankine_mock_data = {
    "hrsg_data": {"mass_flows": {"high_steam": 5, "medium_steam": 3, "low_steam": 2}},
    "pump_data": {"params_operation": {"delta_pressure": 10}},
    "steam_turbine_data": {"low_steam_turbine_params": {"real_quality_outlet_steam": 0.9}},
    "condenser_data": {
      "thermal_change": 1000,
      "saturated_water_mass_flow": 4,
      "make_up_water_mass_flow": 1,
      "cooling_water_mass_flow": 10
    },
    "generated_consumed_powers_data": {
      "gross_power_steam_turbine": 200_000,
      "net_power_steam_turbine": 195_000,
      "consumed_power": 5_000
    }
  }

  cycles_perf_mock_data = {
    "gross_power_combined_cycles": 300_000,
    "net_power_combined_cycles": 295_000,
    "gross_cycle_combined_efficiency": 21.38,
    "net_cycle_combined_efficiency": 21.04
  }

  # --- Monkeypatch of dependent classes ---
  monkeypatch.setattr("app.services.orchestrators.full_cycles.BraytonCycle", lambda *a, **kw: type("", (), {"run": lambda self: brayton_mock_data})())
  monkeypatch.setattr("app.services.orchestrators.full_cycles.RankineCycle", lambda *a, **kw: type("", (), {"run": lambda self: rankine_mock_data})())
  monkeypatch.setattr("app.services.orchestrators.full_cycles.CyclesPerformances", lambda *a, **kw: type("", (), {"cycles_effiencies_calc": lambda self, *b, **kw: cycles_perf_mock_data})())

  # --- Execution ---
  repositories = type("RepoContainer", (), {"substance_repository": None, "icph_repository": None})()
  service = FullCycles(mock_input, repositories)
  result = service.create_full_cycles_combined()

  # --- Validations ---
  assert isinstance(result, FullCyclesResult)
  assert result.LHV_fuel == 500_000_000
  assert result.net_power_cycle_combined == 295_000
  assert result.gross_cycle_combined_efficiency == 21.38
  assert result.net_cycle_combined_efficiency == 21.04
  assert result.exhaustion_gas_temperature == 450.0
  assert result.high_steam_mass_flow == 5
