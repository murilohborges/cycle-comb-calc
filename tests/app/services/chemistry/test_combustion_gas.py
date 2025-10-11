import pytest
from app.services.chemistry.combustion_gas import CombustionGas
from app.utils.errors import NotFoundError

# ---------- Fakes to simulate the repositories ----------
class FakeSubstanceRepo:
  def get_all(self):
    return {
      "oxygen": {"id": 1, "molar_mass": 32.0},
      "nitrogen": {"id": 2, "molar_mass": 28.0},
      "water": {"id": 3, "molar_mass": 18.0},
      "carbon_dioxide": {"id": 4, "molar_mass": 44.0}
    }

class FakeIcphRepo:
    def get_by_substance_id(self, substance_id):
      # simple values for the tests
      return {
        "param_A": float(substance_id),
        "param_B": float(substance_id) * 2,
        "param_C": float(substance_id) * 3,
        "param_D": float(substance_id) * 4,
      }

class FakeInput():
  fuel_mass_flow = 100
  water_molar_fraction_fuel = 2.5
  carbon_dioxide_molar_fraction_fuel = 1.5
  nitrogen_molar_fraction_fuel = 2.0

class FakeInputAir():
  input_air_data = {
      "molar_flow": {"oxygen": 5000, "water": 600, "nitrogen": 7000},
      "fractions": {"oxygen": 0.20, "water": 0.01, "nitrogen": 0.79},
      "molar_mass": 28.8,
      "mass_flow": 50000,
      "icph_params": {"param_A": 1, "param_B": 2, "param_C": 1, "param_D": 1}
    }

class FakeGasFuel():
  gas_fuel_molar_mass = 18.3

class FakeReactions:
  stoichiometric_flow = {
    "oxygen_stoichiometric": 5000,
    "carbon_dioxide_stoichiometric": 4000,
    "water_stoichiometric": 3000
  }



@pytest.fixture
def combustion_gas():
    return CombustionGas(FakeInput(), FakeSubstanceRepo(), FakeIcphRepo())



def test_fraction_molar_calc_valid(combustion_gas):
  """Testing fraction_molar_calc method with valid values"""
  flows = {"oxygen": 2.0, "nitrogen": 6.0}
  result = combustion_gas.fraction_molar_calc(flows)

  assert pytest.approx(result["oxygen"], rel=1e-6) == 0.25
  assert pytest.approx(result["nitrogen"], rel=1e-6) == 0.75
  assert pytest.approx(sum(result.values()), rel=1e-6) == 1.0


def test_fraction_molar_calc_division_by_zero(combustion_gas):
  """Testing fraction_molar_calc method with invalid values"""
  flows = {"oxygen": 0.0, "nitrogen": 0.0}
  with pytest.raises(ZeroDivisionError):
    combustion_gas.fraction_molar_calc(flows)


def test_average_molar_mass_calc_valid(combustion_gas):
  """Testing average_molar_mass_calc method with valid values"""
  fractions = {"oxygen": 0.5, "nitrogen": 0.5}
  result = combustion_gas.average_molar_mass_calc(fractions)

  # weighted average = 0.5*32 + 0.5*28 = 30
  assert pytest.approx(result, rel=1e-6) == 30.0


def test_average_molar_mass_calc_missing_substance(combustion_gas):
  """Testing average_molar_mass_calc method with invalid values"""
  fractions = {"argon": 1.0}  # does not exist in the fake repo
  with pytest.raises(KeyError):
    combustion_gas.average_molar_mass_calc(fractions)


def test_icph_params_calc_valid(combustion_gas):
  """Testing icph_params_calc method with valid values"""
  fractions = {"oxygen": 0.5, "nitrogen": 0.5}
  result = combustion_gas.icph_params_calc(fractions)

  assert set(result.keys()) == {"param_A", "param_B", "param_C", "param_D"}
  assert all(v > 0 for v in result.values())


def test_icph_params_calc_missing(combustion_gas):
  """Testing icph_params_calc method with invalid values"""
  # Simulando repo que não retorna ICPH
  class EmptyIcphRepo:
    def get_by_substance_id(self, _):
      return None

  combustion_gas = CombustionGas(FakeInput(), FakeSubstanceRepo(), EmptyIcphRepo())
  with pytest.raises(NotFoundError):
    combustion_gas.icph_params_calc({"oxygen": 1.0})


def test_gas_combustion_data_calc_valid(combustion_gas):
  """Testing gas_combustion_data_calc method with valid values"""
  stoichiometric_flow = FakeReactions.stoichiometric_flow
  input_air = FakeInputAir.input_air_data
  gas_fuel_molar_mass = FakeGasFuel.gas_fuel_molar_mass
  result = combustion_gas.combustion_gas_data_calc(stoichiometric_flow, input_air, gas_fuel_molar_mass)

  assert "molar_flow" in result
  assert "fractions" in result
  assert "molar_mass" in result
  assert "mass_flow" in result
  assert "icph_params" in result

  # minimum guarantees
  assert pytest.approx(sum(result["fractions"].values()), rel=1e-6) == 1.0
  assert result["mass_flow"] > 0
