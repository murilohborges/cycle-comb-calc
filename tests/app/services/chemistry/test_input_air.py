import pytest
from app.services.chemistry.input_air import InputAir
from app.utils.errors import NotFoundError

# ---------- Fakes to simulate the repositories ----------
class FakeSubstanceRepo:
  def get_all(self):
    return {
      "oxygen": {"id": 1, "molar_mass": 32.0},
      "nitrogen": {"id": 2, "molar_mass": 28.0},
      "water": {"id": 3, "molar_mass": 18.0},
    }

class FakeInvalidSubstanceRepo:
  def get_all(self):
    return 0

class FakeIcphRepo:
  def get_by_substance_id(self, substance_id):
    # simple values for the tests
    return {
      "param_A": float(substance_id),
      "param_B": float(substance_id) * 2,
      "param_C": float(substance_id) * 3,
      "param_D": float(substance_id) * 4,
    }

class FakeInput:
  percent_excess_air = 0


@pytest.fixture
def input_air():
  return InputAir(FakeInput(), FakeSubstanceRepo(), FakeIcphRepo())



def test_fraction_molar_calc_valid(input_air):
  """Testing fraction_molar_calc method with valid values"""
  flows = {"oxygen": 2.0, "nitrogen": 6.0}
  result = input_air.fraction_molar_calc(flows)

  assert pytest.approx(result["oxygen"], rel=1e-6) == 0.25
  assert pytest.approx(result["nitrogen"], rel=1e-6) == 0.75
  assert pytest.approx(sum(result.values()), rel=1e-6) == 1.0


def test_fraction_molar_calc_division_by_zero(input_air):
  """Testing fraction_molar_calc method with invalid values"""
  flows = {"oxygen": 0.0, "nitrogen": 0.0}
  with pytest.raises(ZeroDivisionError):
    input_air.fraction_molar_calc(flows)


def test_average_molar_mass_calc_valid(input_air):
  """Testing average_molar_mass_calc method with valid values"""
  fractions = {"oxygen": 0.5, "nitrogen": 0.5}
  result = input_air.average_molar_mass_calc(fractions)

  # weighted average = 0.5*32 + 0.5*28 = 30
  assert pytest.approx(result, rel=1e-6) == 30.0


def test_average_molar_mass_calc_missing_substance(input_air):
  """Testing average_molar_mass_calc method with invalid values"""
  fractions = {"argon": 1.0}  # does not exist in the fake repo
  with pytest.raises(KeyError):
    input_air.average_molar_mass_calc(fractions)


def test_icph_params_calc_valid(input_air):
  """Testing icph_params_calc method with valid values"""
  fractions = {"oxygen": 0.5, "nitrogen": 0.5}
  result = input_air.icph_params_calc(fractions)

  assert set(result.keys()) == {"param_A", "param_B", "param_C", "param_D"}
  assert all(v > 0 for v in result.values())


def test_icph_params_calc_missing(input_air):
  """Testing icph_params_calc method with invalid values"""
  # Simulating repo that does not return ICPH
  class EmptyIcphRepo:
    def get_by_substance_id(self, _):
      return None

  input_air = InputAir(FakeInput(), FakeSubstanceRepo(), EmptyIcphRepo())
  with pytest.raises(NotFoundError):
    input_air.icph_params_calc({"oxygen": 1.0})


def test_input_air_data_calc_valid(input_air):
  """Testing input_air_data_calc method with valid values"""
  result = input_air.input_air_data_calc(oxygen_stoichiometric=1.0, absolute_humidity=0.01)

  assert "molar_flow" in result
  assert "fractions" in result
  assert "molar_mass" in result
  assert "mass_flow" in result
  assert "icph_params" in result

  # minimum guarantees
  assert pytest.approx(sum(result["fractions"].values()), rel=1e-6) == 1.0
  assert result["mass_flow"] > 0
