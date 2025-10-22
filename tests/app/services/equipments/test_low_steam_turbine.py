import pytest
from math import isclose
from unittest.mock import Mock
from app.utils.errors import ThermodynamicError
from app.services.equipments.low_steam_turbine import LowSteamTurbine

class TestLowSteamTurbine:

  def test_mixing_point_outlet_enthalpy_ok(self):
    """Test mixing point calculation with valid data"""
    turbine = LowSteamTurbine()

    low_steam_enthalpy = 2500
    medium_steam_turbine = {"outlet_enthalpy_real": 3000}
    hrsg_flows = {"medium_steam": 5, "high_steam": 3, "low_steam": 4}

    result = turbine.mixing_point_outlet_enthalpy(low_steam_enthalpy, medium_steam_turbine, hrsg_flows)

    # cálculo manual esperado: ((3000*8 + 2500*4) / 12) = 2833.33
    assert isclose(result, 2833.33, rel_tol=1e-3)

  def test_mixing_point_outlet_enthalpy_invalid_flow(self):
    """Test mixing point calculation with invalid data"""
    turbine = LowSteamTurbine()

    low_steam_enthalpy = 2500
    medium_steam_turbine = {"outlet_enthalpy_real": 3000}
    hrsg_flows = {"medium_steam": 0, "high_steam": 0, "low_steam": 0} # mass flows equal to zero

    with pytest.raises(ZeroDivisionError):
      turbine.mixing_point_outlet_enthalpy(low_steam_enthalpy, medium_steam_turbine, hrsg_flows)


  def test_get_params_operation_normal(self):
    """Test low steam turbine calculation with valid data."""
    turbine = LowSteamTurbine()

    # Input mocks
    input = Mock()
    input.low_steam_level_pressure = 5
    input.low_steam_level_temperature = 300
    input.low_steam_level_efficiency = 80
    input.condenser_operation_pressure = 0.1

    enthalpy = Mock()
    entropy = Mock()
    secant_method = Mock()
    saturation_parameters = Mock()

    # Setting plausible physical returns
    enthalpy.overheated_steam.return_value = 2800
    entropy.overheated_steam.return_value = 6.5
    entropy.saturated_liquid.return_value = 1.0
    entropy.saturated_steam.return_value = 7.0
    enthalpy.saturated_liquid.return_value = 200
    enthalpy.saturated_steam.return_value = 2600
    secant_method.run.return_value = 350

    medium_steam_turbine = {"outlet_enthalpy_real": 3000}
    hrsg_data = {"mass_flows": {"medium_steam": 3, "high_steam": 2, "low_steam": 5}}

    result = turbine.get_params_operation(
      input, saturation_parameters, entropy, enthalpy, medium_steam_turbine, hrsg_data, secant_method
    )

    assert "delta_enthalpy_real" in result
    assert "outlet_enthalpy_real" in result
    assert "real_quality_outlet_steam" in result
    assert isinstance(result["real_quality_outlet_steam"], float)
  
  def test_get_params_operation_invalid_entropy(self):
    """Test low steam turbine calculation with invalid data, saturated entropy equal, division by zero."""
    turbine = LowSteamTurbine()

    input = Mock()
    input.low_steam_level_pressure = 5
    input.low_steam_level_temperature = 300
    input.low_steam_level_efficiency = 80
    input.condenser_operation_pressure = 0.1

    enthalpy = Mock()
    entropy = Mock()
    secant_method = Mock()
    saturation_parameters = Mock()

    # Returns configured with physical error: equal entropies
    enthalpy.overheated_steam.return_value = 2800
    entropy.overheated_steam.return_value = 6.5
    entropy.saturated_liquid.return_value = 5.0
    entropy.saturated_steam.return_value = 5.0  # causes division by zero
    enthalpy.saturated_liquid.return_value = 200
    enthalpy.saturated_steam.return_value = 2600
    secant_method.run.return_value = 350

    medium_steam_turbine = {"outlet_enthalpy_real": 3000}
    hrsg_data = {"mass_flows": {"medium_steam": 3, "high_steam": 2, "low_steam": 5}}

    with pytest.raises(ZeroDivisionError):
      turbine.get_params_operation(
        input, saturation_parameters, entropy, enthalpy, medium_steam_turbine, hrsg_data, secant_method
      )
  
  def test_get_params_operation_superheated_outlet(monkeypatch):
    """Test low steam turbine calculation with invalid data, outlet steam is overheated"""
    turbine = LowSteamTurbine()

    input = Mock()
    input.low_steam_level_pressure = 4
    input.low_steam_level_temperature = 312.5
    input.low_steam_level_efficiency = 90
    input.condenser_operation_pressure = 1 # Operation pressure is too high

    enthalpy = Mock()
    entropy = Mock()
    secant_method = Mock()
    saturation_parameters = Mock()

    enthalpy.overheated_steam.return_value = 3095
    entropy.overheated_steam.return_value = 7.62
    entropy.saturated_liquid.return_value = 1.3
    entropy.saturated_steam.return_value = 7.3
    enthalpy.saturated_liquid.return_value = 420
    enthalpy.saturated_steam.return_value = 2600
    secant_method.run.return_value = 313.5

    medium_steam_turbine = {"outlet_enthalpy_real": 3098}
    hrsg_data = {"mass_flows": {"medium_steam": 3, "high_steam": 2, "low_steam": 5}}

    with pytest.raises(ThermodynamicError) as excinfo:
      turbine.get_params_operation(input, saturation_parameters, entropy, enthalpy, medium_steam_turbine, hrsg_data, secant_method
  )

    assert "The outlet steam in the low steam turbine is still overheated or saturated, review the conditions of the power plant" in str(excinfo.value)