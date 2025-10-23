import pytest
from app.services.equipments.condenser import Condenser
from app.utils.errors import ThermodynamicError

class MockInput:
  condenser_operation_pressure = 0.1  # MPa
  range_temperature_cooling_tower = 10  # °C

class MockSubstanceRepo:
  def get_all(self):
    return {"water": {"molar_mass": 18.015}}  # g/mol

class MockEnthalpy:
  def saturated_liquid(self, pressure):
    # Returns typical enthalpy of saturated water
    return 191.8  # kJ/kg

class TestCondenser:
  def test_get_params_operation_normal(self):
    """Test condenser calculation with valid data."""
    condenser = Condenser()
    input = MockInput()
    substance_repo = MockSubstanceRepo()
    enthalpy = MockEnthalpy()

    steam_turbine_hrsg_data = {
      "steam_turbine_data": {
        "low_steam_turbine_params": {
          "outlet_enthalpy_real": 2200  # kJ/kg
        }
      },
      "hrsg_data": {
        "mass_flows": {
          "total_steam_generated": 100,  # kg/s
          "purge": 2                    # kg/s
        }
      }
    }

    result = condenser.get_params_operation(input, substance_repo, enthalpy, steam_turbine_hrsg_data)

    assert "thermal_change" in result
    assert "cooling_water_mass_flow" in result
    assert result["thermal_change"] > 0
    assert result["cooling_water_mass_flow"] > 0

  def test_get_params_operation_missing_key(self):
    """Test condenser calculation with invalid data, missing dict key."""
    condenser = Condenser()
    input = MockInput()
    substance_repo = MockSubstanceRepo()
    enthalpy = MockEnthalpy()

    # Missing block "low_steam_turbine_params"
    steam_turbine_hrsg_data = {
      "steam_turbine_data": {},
      "hrsg_data": {
        "mass_flows": {
          "total_steam_generated": 100,
          "purge": 2
        }
      }
    }

    with pytest.raises(KeyError):
      condenser.get_params_operation(input, substance_repo, enthalpy, steam_turbine_hrsg_data)

  def test_get_params_operation_invalid_pressure(self):
    """Test condenser calculation with invalid data, operation pressure equal to zero."""
    condenser = Condenser()
    substance_repo = MockSubstanceRepo()
    enthalpy = MockEnthalpy()

    class InvalidInput:
      condenser_operation_pressure = 0  # Invalid pressure
      range_temperature_cooling_tower = 10

    input = InvalidInput()

    steam_turbine_hrsg_data = {
      "steam_turbine_data": {
        "low_steam_turbine_params": {
          "outlet_enthalpy_real": 2200
        }
      },
      "hrsg_data": {
        "mass_flows": {
          "total_steam_generated": 100,
          "purge": 2
        }
      }
    }

    with pytest.raises(ThermodynamicError):
      condenser.get_params_operation(input, substance_repo, enthalpy, steam_turbine_hrsg_data)