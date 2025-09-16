import pytest
import math
from unittest.mock import Mock
from app.services.thermodynamics.steam.enthalpy import Enthalpy


@pytest.fixture
def mock_saturation_parameters():
    mock = Mock()
    # by default, it returns 100 °C (373.15 K) as the saturation temperature
    mock.saturation_temperature.return_value = 100  
    # default factor returns 1 for simplicity
    mock.saturation_factor.return_value = 1  
    return mock


class TestEnthalpy:

  # ---------- TESTS FOR saturated liquid ----------
  def test_saturated_liquid_valid(self, mock_saturation_parameters):
    """Test saturated_liquid calculation with valid data."""
    enthalpy = Enthalpy()
    result = enthalpy.saturated_liquid(pressure=1, saturation_parameters=mock_saturation_parameters)

    # Since the factor returned 1, the result should be equal to the critical_point_enthalpy defined in the range (2099.3)
    assert math.isclose(result, 2099.3, rel_tol=1e-5)

  def test_saturated_liquid_invalid_pressure(self, mock_saturation_parameters):
    """Test saturated_liquid calculation with invalid data."""
    enthalpy = Enthalpy()
    # Force value out of range (< 273.16 K or > 647.3 K)
    mock_saturation_parameters.saturation_temperature.return_value = -300  

    with pytest.raises(ValueError, match="Pressure invalid: out of the range"):
      enthalpy.saturated_liquid(pressure=1, saturation_parameters=mock_saturation_parameters)

  # ---------- TESTS FOR saturated steam ----------
  def test_saturated_steam_valid(self, mock_saturation_parameters):
    """Test saturated_steam calculation with valid data."""
    enthalpy = Enthalpy()
    result = enthalpy.saturated_steam(pressure=1, saturation_parameters=mock_saturation_parameters)

    # Since the factor returns 1, it must be equal to the critical_point_enthalpy
    assert math.isclose(result, 2099.3, rel_tol=1e-5)

  def test_saturated_steam_invalid_factor(self, mock_saturation_parameters):
    """Test saturated_steam calculation with invalid data."""
    enthalpy = Enthalpy()
    mock_saturation_parameters.saturation_factor.return_value = float("nan")

    result = enthalpy.saturated_steam(pressure=1, saturation_parameters=mock_saturation_parameters)
    assert math.isnan(result)

  # ---------- TESTES PARA overheated_steam ----------
  def test_overheated_steam_valid(self, mock_saturation_parameters):
    """Test overheated_steam calculation with valid data."""
    enthalpy = Enthalpy()
    mock_saturation_parameters.saturation_temperature.return_value = 100  # 100 °C

    result = enthalpy.overheated_steam(pressure=10, temperature=200, saturation_parameters=mock_saturation_parameters)

    assert isinstance(result, float)
    assert result != 0  # must generate a valid numeric value

  def test_overheated_steam_temperature_equal_saturation(self, mock_saturation_parameters):
    """Test overheated_steam calculation with valid and extreme data."""
    enthalpy = Enthalpy()
    # Extreme case: T == T_sat => exp(0) = 1
    mock_saturation_parameters.saturation_temperature.return_value = 200

    result = enthalpy.overheated_steam(pressure=10, temperature=200, saturation_parameters=mock_saturation_parameters)
    assert isinstance(result, float)

  def test_overheated_steam_invalid_pressure(self, mock_saturation_parameters):
    """Test overheated_steam calculation with invalid data."""
    enthalpy = Enthalpy()
    mock_saturation_parameters.saturation_temperature.return_value = 100

    # negative pressure -> may give strange results
    result = enthalpy.overheated_steam(pressure=-5, temperature=200,saturation_parameters=mock_saturation_parameters)

    assert isinstance(result, float)
