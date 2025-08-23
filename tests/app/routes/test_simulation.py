import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.input import Input
from app.models.output import Output

client = TestClient(app)

def test_create_simulation_route():
  """
  Testing '/simulation' endpoint route
  """
  payload = Input(
    methane_molar_fraction_fuel=87.08,
    ethane_molar_fraction_fuel=7.83,
    propane_molar_fraction_fuel=2.94,
    n_butane_molar_fraction_fuel=0,
    water_molar_fraction_fuel=0,
    carbon_dioxide_molar_fraction_fuel=0.68,
    hydrogen_molar_fraction_fuel=0,
    nitrogen_molar_fraction_fuel=1.47,
    fuel_mass_flow=53064,
    fuel_input_temperature=25,
    air_input_temperature=25,
    percent_excess_air=164.15,
    local_atmospheric_pressure=1,
    relative_humidity=60,
    gas_turbine_efficiency=36.78,
    chimney_gas_temperature=99.7,
    purge_level=0,
    high_steam_level_pressure=98.8,
    medium_steam_level_pressure=24,
    low_steam_level_pressure=4,
    high_steam_level_temperature=565,
    medium_steam_level_temperature=565,
    low_steam_level_temperature=312.5,
    high_steam_level_fraction=70,
    medium_steam_level_fraction=15,
    high_steam_level_efficiency=87,
    medium_steam_level_efficiency=91,
    low_steam_level_efficiency=89,
    reductor_generator_set_efficiency=98.5,
    pump_efficiency=75,
    engine_pump_efficiency=82.5,
    power_factor_pump_efficiency=0.84,
    condenser_operation_pressure=0.074,
    range_temperature_cooling_tower=10
  )

  response = client.post("/simulation", json=payload.model_dump())
  assert response.status_code == 200

  # Response validation with Output model pydantic
  validated_output = Output(**response.json())

  assert isinstance(validated_output, Output)

