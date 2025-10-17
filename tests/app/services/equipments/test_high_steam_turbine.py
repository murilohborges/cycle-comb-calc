import pytest
from unittest.mock import Mock
from app.utils.errors import ThermodynamicError
from app.services.equipments.high_steam_turbine import HighSteamTurbine

class TestHighSteamTurbine:

  def test_get_params_operation_normal():
    """Test high steam turbine calculation with valid data."""
    turbine = HighSteamTurbine()

    # Input mocks
    input_mock = Mock()
    input_mock.high_steam_level_pressure = 10
    input_mock.high_steam_level_temperature = 500
    input_mock.high_steam_level_efficiency = 85
    input_mock.medium_steam_level_pressure = 5

    saturation_parameters = Mock()
    saturation_parameters.saturation_temperature.return_value = 180.5

    entropy = Mock()
    entropy.overheated_steam.side_effect = [6.7, 6.0]  # inlet e outlet

    enthalpy = Mock()
    enthalpy.overheated_steam.side_effect = [3500, 3000]  # inlet e outlet

    secant_method = Mock()
    secant_method.run.return_value = 350  # estimated outlet temperature

    result = turbine.get_params_operation(input_mock, saturation_parameters, entropy, enthalpy, secant_method)

    # Checks
    assert "delta_enthalpy_real" in result
    assert "outlet_enthalpy_real" in result
    assert isinstance(result["outlet_enthalpy_real"], (float, int))

  def test_get_params_operation_below_saturation_temperature():
    """Test high steam turbine calculation with invalid data, incorrect input temperature."""
    turbine = HighSteamTurbine()

    # Input mocks
    input_mock = Mock()
    input_mock.high_steam_level_pressure = 10
    input_mock.high_steam_level_temperature = 150  # below saturation
    input_mock.high_steam_level_efficiency = 85
    input_mock.medium_steam_level_pressure = 5

    saturation_parameters = Mock()
    saturation_parameters.saturation_temperature.return_value = 180.5

    entropy = Mock()
    enthalpy = Mock()
    secant_method = Mock()

    # Expected to throw custom exception
    with pytest.raises(ThermodynamicError) as excinfo:
      turbine.get_params_operation(input_mock, saturation_parameters, entropy, enthalpy, secant_method)

    assert "below saturation" in str(excinfo.value)