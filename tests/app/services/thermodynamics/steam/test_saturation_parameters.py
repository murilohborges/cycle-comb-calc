import pytest
import math
from app.services.thermodynamics.steam.saturation_parameters import SaturationParameters
from app.utils.errors import DataValidationError

class TestSaturationParameters:

    def setup_method(self):
        self.sp = SaturationParameters()

    # -------------------------------
    # saturation_temperature
    # -------------------------------
    def test_saturation_temperature_low_pressure(self):
      # Example: pressure in first range
      Tsat = self.sp.saturation_temperature(1) # 1 bar
      assert isinstance(Tsat, float)

      # Value of literature
      expected = 372.87 - 273.15
      assert pytest.approx(Tsat, rel=1e-2) == expected

    def test_saturation_temperature_high_pressure(self):
      # Example: pressure in second range
      Tsat = self.sp.saturation_temperature(200)  # 200 bar

      # Value of literature
      expected = 638.95 - 273.15
      assert pytest.approx(Tsat, rel=1e-2) == expected

    def test_saturation_temperature_invalid_pressure(self):
      # Example: pressure out of range
      with pytest.raises(DataValidationError):
        self.sp.saturation_temperature(0.0001)

    # -------------------------------
    # saturation_pressure
    # -------------------------------
    def test_saturation_pressure_valid_temp(self):
        Psat = self.sp.saturation_pressure(100)  # 100 °C
        assert isinstance(Psat, float)
        # Value of literature
        expected = 0.1014 * 10
        assert pytest.approx(Psat, rel=1e-2) == expected

    def test_saturation_pressure_invalid_temp(self):
        # Example: temperature out of range
        with pytest.raises(DataValidationError):
            self.sp.saturation_pressure(-200)  # fora da faixa

    # -------------------------------
    # saturation_factor
    # -------------------------------
    def test_saturation_factor_valid(self):
        result = self.sp.saturation_factor(
            saturation_temp=100,
            A=1, B=0.1, C=0.01, D=0.001,
            E1=0.001, E2=0.0001, E3=0.00001,
            E4=0.000001, E5=0.0000001, E6=0.00000001, E7=0.000000001
        )
        assert isinstance(result, float)

    def test_saturation_factor_different_temp(self):
        result1 = self.sp.saturation_factor(50, 1,0.1,0.01,0.001,0,0,0,0,0,0,0)
        result2 = self.sp.saturation_factor(150, 1,0.1,0.01,0.001,0,0,0,0,0,0,0)
        assert result1 != result2  # values ​​should change according to temperature
