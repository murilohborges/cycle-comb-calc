import re
import pytest
from app.services.utils.secant_method import SecantMethod
from app.utils.errors import ComputationalError

class MockSaturationParameters:
  """Mock that simulates the behavior of the saturation object"""
  def saturation_temperature(self, pressure):
    # fixed value just to simplify the test
    return 100.0


class MockThermoPropertyFunction:
  """Mock that simulates the thermodynamic function used in the iterations"""
  def __init__(self, variation_factor=0.5):
    self.variation_factor = variation_factor

  def overheated_steam(self, pressure, temperature):
    # simulated function with simple linear relationship
    # the higher the temperature, the higher the returned value
    return pressure * 0.1 + (temperature - 2.71) * self.variation_factor

def test_secant_method_converges_successfully():
  """Test secant_method calculation with valid data."""
  secant = SecantMethod()
  mock_saturation = MockSaturationParameters()
  mock_thermo = MockThermoPropertyFunction()

  # inlet_property should be similar to the expected output (to facilitate convergence)
  inlet_property = 5.0
  outlet_pressure = 10.0

  result = secant.run(inlet_property, mock_thermo, outlet_pressure, mock_saturation)

  # Since we are only testing the execution, we expect the result to be numeric and positive.
  assert isinstance(result, float)
  assert result > 0
  # And that it has converged (tolerance < 0.01)
  # In this case, since we don't have internal access to the tolerance, we just need to ensure that it didn't exceed 100 iterations
  # (the function returned successfully)

def test_secant_method_fails_to_converge():
  """Test secant_method calculation with Bad Thermo Function what returns a constant value."""
  secant = SecantMethod()
  mock_saturation = MockSaturationParameters()

  class BadThermoFunction:
    def overheated_steam(self, pressure, temperature):
      # Always returns the same value → prevents convergence
      return 1.0

  bad_thermo = BadThermoFunction()

  expected_message = "Secant method failed: no variation between iterations (possible flat function)"

  # we intercept possible divisions by zero or loops without convergence
  with pytest.raises(ComputationalError, match=re.escape(expected_message)):
    secant.run(
      inlet_property=5.0,
      thermo_property_function=bad_thermo,
      outlet_pressure=10.0,
      saturation_parameters=mock_saturation
    )
