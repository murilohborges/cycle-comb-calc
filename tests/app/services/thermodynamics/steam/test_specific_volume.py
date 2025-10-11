import pytest
import math
from unittest.mock import Mock
from app.services.thermodynamics.steam.specific_volume import SpecificVolume


@pytest.fixture
def mock_saturation_parameters():
  mock = Mock()
  # by default, return 100 °C as saturation temperature
  mock.saturation_temperature.return_value = 100
  # default factor returns 1
  mock.saturation_factor.return_value = 1
  return mock


class TestSpecificVolume:

  # ---------- TESTS FOR saturated_liquid ----------
  def test_saturated_liquid_valid(self, mock_saturation_parameters):
    """Test saturated_liquid calculation with valid data."""
    specific_volume = SpecificVolume(saturation_params=mock_saturation_parameters)
    result = specific_volume.saturated_liquid(pressure=1)

    # Since factor = 1, result should equal critical_point_entropy
    assert math.isclose(result, 0.003155, rel_tol=1e-5)

  def test_saturated_liquid_invalid_pressure(self, mock_saturation_parameters):
    """Test saturated_liquid calculation with invalid data."""
    # Force out-of-range value
    mock_saturation_parameters.saturation_temperature.return_value = -300
    specific_volume = SpecificVolume(saturation_params=mock_saturation_parameters)

    with pytest.raises(ValueError, match="Pressure invalid: out of the range"):
      specific_volume.saturated_liquid(pressure=1)
