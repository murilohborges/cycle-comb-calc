import pytest
from app.services.thermodynamics.psychrometry.humidity import Humidity

class TestHumidity:
  @pytest.mark.parametrize(
        "saturation_pressure, local_pressure, rh, expected",
        [
            (0.0171, 1.0, 60, 0.0063),   # valid case (literature)
            (0.0171, 1.0, 0, 0.0),       # zero relative humidity
            (0.0171, 1.0, 100, 0.0107),  # saturated (approximate value)
        ]
    )

  def test_absolute_humidity_calc(self, saturation_pressure, local_pressure, rh, expected):
    """
    Test Absolute humidity calculation of the local atmosphere with valid data.
    """

    # Instance of class
    humidity = Humidity()
    result = humidity.absolute_humidity_calc(saturation_pressure, local_pressure, rh)

    assert pytest.approx(result, abs=1e-3) == expected
