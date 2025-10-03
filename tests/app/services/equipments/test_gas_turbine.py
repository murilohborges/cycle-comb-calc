import pytest
from app.services.equipments.gas_turbine import GasTurbine
from app.services.configs.gas_turbine_config import GasTurbineConfig

# ---------- Fakes for dependencies ----------

class FakeInput:
  fuel_mass_flow = 100
  fuel_input_temperature = 300
  air_input_temperature = 290
  gas_turbine_efficiency = 35
  local_temperature = 298.15
  local_atmospheric_pressure = 1.0
  relative_humidity = 50

class FakeGasFuel:
  def LHV_fuel_calc(self):
    return 50000

  def fractions(self):
    return {"methane": 0.9, "ethane": 0.1}

  def icph_params_calc(self):
    return {"param_A": 1, "param_B": 2, "param_C": 3, "param_D": 4}

  def average_molar_mass_calc(self):
    return 20.0

class FakeICPH:
  def icph_calc_heat(self, params, molar_mass, T, T_ref):
    return 100.0

class FakeReactions:
  def molar_flow_stoichiometric_calc(self):
    return {"oxygen_stoichiometric": 100, "carbon_dioxide_stoichiometric": 200}

class FakeInputAir:
  def input_air_data_calc(self, oxygen_stoichiometric, abs_humidity):
    return {
      "molar_flow": {"oxygen": 100, "nitrogen": 200, "water": 10},
      "fractions": {"oxygen": 0.25, "nitrogen": 0.70, "water": 0.05},
      "molar_mass": 29.0,
      "mass_flow": 1000,
      "icph_params": {"param_A": 1, "param_B": 2, "param_C": 3, "param_D": 4},
    }

class FakeCombustionGas:
  def combustion_gas_data_calc(self, stoich, input_air, molar_mass):
    return {
      "molar_flow": {"co2": 100, "h2o": 50},
      "fractions": {"co2": 0.6, "h2o": 0.4},
      "molar_mass": 28.0,
      "mass_flow": 200,
      "icph_params": {"param_A": 1, "param_B": 2, "param_C": 3, "param_D": 4},
    }

class FakeHumidity:
  def absolute_humidity_calc(self, ps, patm, rh):
    return 0.01

class FakeSaturation:
  def saturation_pressure(self, T):
    return 0.02

class FakeSubstanceRepo:
  def get_all(self):
    return {"oxygen": {"id": 1, "molar_mass": 32.0}}

class FakeIcphRepo:
  def get_by_substance_id(self, substance_id):
    return {"param_A": 1, "param_B": 2, "param_C": 3, "param_D": 4}

# ---------- Main fixture ----------
@pytest.fixture
def gas_turbine():
  # Creates all fake instances
  fake_input = FakeInput()
  fake_gas_fuel = FakeGasFuel()
  fake_icph = FakeICPH()
  fake_reactions = FakeReactions()
  fake_input_air = FakeInputAir()
  fake_combustion_gas = FakeCombustionGas()
  fake_humidity = FakeHumidity()
  fake_saturation = FakeSaturation()
  fake_substance_repo = FakeSubstanceRepo()
  fake_icph_repo = FakeIcphRepo()

  # Build the config
  config = GasTurbineConfig(
    input=fake_input,
    gas_fuel=fake_gas_fuel,
    icph=fake_icph,
    substance_repo=fake_substance_repo,
    icph_repo=fake_icph_repo,
    reactions=fake_reactions,
    input_air=fake_input_air,
    combustion_gas=fake_combustion_gas,
    humidity=fake_humidity,
    saturation_parameters=fake_saturation
  )

  # Instancia o GasTurbine com a config
  return GasTurbine(config)

# ---------- TESTS ----------

# fuel_sensible_heat_calc
def test_fuel_sensible_heat_calc_valid(gas_turbine):
  """Testing fuel_sensible_heat_calc method with valid values"""
  result = gas_turbine.fuel_sensible_heat_calc()
  assert isinstance(result, (int, float))
  assert result == 100.0  # mock value in FakeICPH.icph_calc_heat

# net_power_GT_calculation
def test_net_power_GT_calculation_valid(gas_turbine):
  """Testing net_power_GT_calculation method with valid values"""
  result = gas_turbine.net_power_GT_calculation()
  assert result > 0

def test_net_power_GT_calculation_zero_efficiency(gas_turbine):
  """Testing net_power_GT_calculation method with invalid values, gas_turbine_efficiency = 0 """
  gas_turbine.input.gas_turbine_efficiency = 0
  with pytest.raises(ZeroDivisionError):
    gas_turbine.net_power_GT_calculation()

# input_air_properties
def test_input_air_properties_valid(gas_turbine):
  """Testing input_air_properties method with valid values"""
  result = gas_turbine.input_air_properties()
  assert "molar_flow" in result
  assert result["mass_flow"] > 0

def test_input_air_properties_invalid_humidity(gas_turbine):
  """Testing input_air_properties method with invalid values, with infinity absolute humidity value"""
  gas_turbine.input_air.input_air_data_calc = lambda *a, **kw: None
  result = gas_turbine.input_air_properties()
  assert result is None


# combustion_gas_properties
def test_combustion_gas_properties_valid(gas_turbine):
  """Testing combustion_gas_properties method with valid values"""
  result = gas_turbine.combustion_gas_properties()
  assert "molar_flow" in result
  assert result["mass_flow"] > 0

def test_combustion_gas_properties_invalid(gas_turbine):
  """Testing combustion_gas_properties method with invalid values, with infinity absolute humidity value"""
  gas_turbine.combustion_gas.combustion_gas_data_calc = lambda *a, **kw: None
  result = gas_turbine.combustion_gas_properties()
  assert result is None

# exhaustion_gas_temp
def test_exhaustion_gas_temp_valid(gas_turbine):
  result = gas_turbine.exhaustion_gas_temp()
  assert result > 0  # temperature in °C

def test_exhaustion_gas_temp_invalid_zero_mass(gas_turbine):
  gas_turbine.combustion_gas.combustion_gas_data_calc = lambda *a, **kw: {
    "molar_mass": 0,
    "mass_flow": 0,
    "icph_params": {"param_A": 0, "param_B": 0, "param_C": 0, "param_D": 0},
  }
  with pytest.raises(ZeroDivisionError):
    gas_turbine.exhaustion_gas_temp()

