import pytest
from app.services.thermodynamics.heat.icph import ICPH

class TestICPH:
  def test_icph_heat_calc(self):
    """
    Test ICPH heat calculation of gas fuel with valid data.
    """
    # Creating mock with icph params
    mock_icph_params = {"param_A": 3.426, "param_B": 6.71e-4, "param_C": 0, "param_D": -3.35e3}

    # Others params of icph_calc_heat
    temp_in = 35
    temp_out = 30
    molar_mass = 18.5

    service = ICPH()
    result = service.icph_calc_heat(mock_icph_params, molar_mass, temp_in, temp_out)

    # Expected value of literature
    expected = -8.08

    assert pytest.approx(result, rel=1e-2) == expected
  
  def test_icph_zero_when_same_temp(self):
    """
    Test ICPH heat calculation of gas fuel with the same temperature in and out.
    """
    icph = ICPH()
    icph_params = {"param_A": 1.0, "param_B": 1.0, "param_C": 1.0, "param_D": 1.0}
    result = icph.icph_calc_heat(icph_params, molar_mass=28.97, temp_in=25, temp_out=25)
    assert result == 0.0

  def test_icph_positive_heat(self):
    """
    Test ICPH heat calculation of gas fuel to check result is positive.
    """
    icph = ICPH()
    icph_params = {"param_A": 1.0, "param_B": 1.0, "param_C": 1.0, "param_D": 1.0}
    result = icph.icph_calc_heat(icph_params, molar_mass=28.97, temp_in=25, temp_out=100)
    assert result > 0