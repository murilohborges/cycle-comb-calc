import pytest
import numpy as np
from unittest.mock import Mock
from app.services.equipments.HRSG import HRSG  


class TestHRSG:

  # ---------- Test for heat_supplied_calc ----------
  def test_heat_supplied_calc_normal(self):
    hrsg = HRSG()
    input_mock = Mock(chimney_gas_temperature=120)
    combustion_gas = {
      "icph_params": {"param": 1},
      "molar_mass": 28.97,
      "mass_flow": 2.0
    }
    icph_mock = Mock()
    icph_mock.icph_calc_heat.return_value = 150.0

    result = hrsg.heat_supplied_calc(input_mock, combustion_gas, exhaustion_temp=500, icph=icph_mock)

    icph_mock.icph_calc_heat.assert_called_once()
    assert result == abs(150.0 * 2.0)  # expected: 300.0

  # ---------- Test for get_params_operation ----------
  def test_get_params_operation_normal(self):
    hrsg = HRSG()
    input_mock = Mock(
      high_steam_level_pressure=10,
      high_steam_level_temperature=500,
      medium_steam_level_pressure=5,
      medium_steam_level_temperature=350,
      low_steam_level_pressure=2,
      low_steam_level_temperature=250
    )
    saturation_params = Mock()
    saturation_params.saturation_temperature.side_effect = [180.87944, 200.418784, 220.5198798]
    enthalpy_calc = Mock()
    enthalpy_calc.overheated_steam.side_effect = [3100, 2900, 2700]
    enthalpy_calc.saturated_liquid.side_effect = [800, 700, 600]

    high_steam_turbine = {"outlet_enthalpy_real": 2500}
    pump = {"outlet_real_enthalpy": 500}

    result = hrsg.get_params_operation(input_mock, saturation_params, enthalpy_calc, high_steam_turbine, pump)

    assert result["high_steam_enthaply"] == 3100
    assert result["medium_purge_enthalpy"] == 700
    assert result["inlet_water_enthalpy"] == 500

  # ---------- Test for get_mass_flow ----------
  def test_get_mass_flow_normal(self):
    hrsg = HRSG()
    input_mock = Mock(
      high_steam_level_fraction=50,
      medium_steam_level_fraction=30,
      purge_level=10
    )

    hsrg_params = {
      "high_steam_enthaply": 3100,
      "medium_steam_enthaply": 2900,
      "low_steam_enthaply": 2700,
      "high_purge_enthalpy": 800,
      "medium_purge_enthalpy": 700,
      "low_purge_enthalpy": 600,
      "medium_steam_cold_enthaply": 2600,
      "inlet_water_enthalpy": 500
    }

    heat_supplied = 1e6  # 1000000 kJ/h

    result = hrsg.get_mass_flow(input_mock, hsrg_params, heat_supplied)

    assert "total_steam_generated" in result
    assert result["feed_water_required"] > 0
    assert np.isclose(result["high_steam"], result["total_steam_generated"] * 0.5)

  def test_get_mass_flow_singular_matrix(self):
    hrsg = HRSG()
    input_mock = Mock(
      high_steam_level_fraction=50,
      medium_steam_level_fraction=30,
      purge_level=10
    )

    hsrg_params = {
      # Values ​​created to generate singular matrix (A non-invertible)
      "high_steam_enthaply": 0,
      "medium_steam_enthaply": 0,
      "low_steam_enthaply": 0,
      "high_purge_enthalpy": 0,
      "medium_purge_enthalpy": 0,
      "low_purge_enthalpy": 0,
      "medium_steam_cold_enthaply": 0,
      "inlet_water_enthalpy": 0
    }

    with pytest.raises(np.linalg.LinAlgError):
      hrsg.get_mass_flow(input_mock, hsrg_params, heat_supplied=0)
