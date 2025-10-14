import pytest
import math
from unittest.mock import Mock
from app.services.thermodynamics.steam.entropy import Entropy
from app.utils.errors import DataValidationError

@pytest.fixture
def mock_saturation_parameters():
  mock = Mock()
  # by default, return 100 °C as saturation temperature
  mock.saturation_temperature.return_value = 100
  # default factor returns 1
  mock.saturation_factor.return_value = 1
  return mock


class TestEntropy:

  # ---------- TESTS FOR saturated_liquid ----------
  def test_saturated_liquid_valid(self):
    """Test saturated_liquid calculation with valid data."""
    entropy = Entropy()
    result = entropy.saturated_liquid(pressure=1)

    assert math.isclose(result, 1.3050, rel_tol=1e-2)

  def test_saturated_liquid_invalid_pressure(self, mock_saturation_parameters):
    """Test saturated_liquid calculation with invalid data."""
    # Force out-of-range value
    mock_saturation_parameters.saturation_temperature.return_value = -300
    entropy = Entropy(saturation_params=mock_saturation_parameters)

    with pytest.raises(DataValidationError, match="Pressure invalid: out of the range"):
      entropy.saturated_liquid(pressure=1)

  # ---------- TESTS FOR saturated_steam ----------
  def test_saturated_steam_valid(self):
    """Test saturated_steam calculation with valid data."""
    entropy = Entropy()
    result = entropy.saturated_steam(pressure=1)

    # Since factor = 1, result should equal critical_point_entropy
    assert math.isclose(result, 7.3568, rel_tol=1e-2)

  def test_saturated_steam_invalid_factor(self, mock_saturation_parameters):
    """Test saturated_steam calculation with invalid data."""
    # Force out-of-range value
    mock_saturation_parameters.saturation_temperature.return_value = -300
    entropy = Entropy(saturation_params=mock_saturation_parameters)

    with pytest.raises(DataValidationError, match="Pressure invalid: out of the range"):
      entropy.saturated_liquid(pressure=1)

  # ---------- TESTS FOR overheated_steam ----------
  def test_overheated_steam_valid(self):
    """Test overheated_steam calculation with valid data."""
    entropy = Entropy()

    result = entropy.overheated_steam(pressure=10, temperature=200)

    assert isinstance(result, float)
    assert result != 0

  def test_overheated_steam_temperature_equal_saturation(self, mock_saturation_parameters):
    """Test overheated_steam calculation with valid and edge data."""
    # Edge case: T == T_sat
    mock_saturation_parameters.saturation_temperature.return_value = 200
    entropy = Entropy(saturation_params=mock_saturation_parameters)

    result = entropy.overheated_steam(pressure=10, temperature=200)

    assert isinstance(result, float)

  def test_overheated_steam_invalid_pressure(self):
    """Test overheated_steam calculation with invalid data."""
    entropy = Entropy()

    # Negative pressure -> math.log() domain error
    with pytest.raises(DataValidationError, match="Pressure invalid: out of the range"):
      entropy.overheated_steam(pressure=-5, temperature=200)
