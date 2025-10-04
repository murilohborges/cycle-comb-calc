import pytest
from app.services.configs.gas_turbine_config import GasTurbineConfig

def test_gasturbineconfig_initialization():
  # Creating fakes/mocks
  fake_input = {"fuel_mass_flow": 100}
  fake_gas_fuel = object()
  fake_icph = object()
  fake_substance_repo = object()
  fake_icph_repo = object()
  fake_reactions = object()
  fake_input_air = object()
  fake_combustion_gas = object()
  fake_humidity = object()
  fake_saturation_parameters = object()

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
    saturation_parameters=fake_saturation_parameters
  )

  # Testing if attributes were stored correctly
  assert config.input == fake_input
  assert config.gas_fuel is fake_gas_fuel
  assert config.icph is fake_icph
  assert config.substance_repo is fake_substance_repo
  assert config.icph_repo is fake_icph_repo
  assert config.reactions is fake_reactions
  assert config.input_air is fake_input_air
  assert config.combustion_gas is fake_combustion_gas
  assert config.humidity is fake_humidity
  assert config.saturation_parameters is fake_saturation_parameters
