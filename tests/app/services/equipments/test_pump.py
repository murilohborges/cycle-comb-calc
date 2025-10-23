import pytest
from app.services.equipments.pump import Pump
from app.utils.errors import ThermodynamicError

class MockInput:
  high_steam_level_pressure = 100  # bar
  condenser_operation_pressure = 0.1  # bar
  pump_efficiency = 85  # %

class MockEnthalpy:
  def saturated_liquid(self, pressure):
    # Exemplo simplificado
    return 191.8  # kJ/kg

class MockSpecificVolume:
  def saturated_liquid(self, pressure):
    return 0.001  # m³/kg (aprox. para água líquida)

class TestPump:
  def test_pump_get_params_operation_normal(self):
    """Test pump calculation with valid data."""
    pump = Pump()
    input = MockInput()
    enthalpy = MockEnthalpy()
    specific_volume = MockSpecificVolume()

    result = pump.get_params_operation(input, enthalpy, specific_volume)

    assert "outlet_real_enthalpy" in result
    assert "delta_pressure" in result
    assert result["delta_specific_enthalpy"] > 0
    assert result["delta_pressure"] > 0
  
  def test_pump_outlet_pressure_less_than_inlet(self):
    """Test pump calculation with invalid data"""
    """Inconsistent pressures: inlet pressure are less than outlet pressure."""
    pump = Pump()
    enthalpy = MockEnthalpy()
    specific_volume = MockSpecificVolume()

    class InvalidInput:
      high_steam_level_pressure = 15  # bar
      condenser_operation_pressure = 40  # bar
      pump_efficiency = 85  # %

    input = InvalidInput()

    with pytest.raises(ThermodynamicError):
      pump.get_params_operation(input, enthalpy, specific_volume)
  
  def test_pump_outlet_pressure_equal_to_inlet(self):
    """Test pump calculation with invalid data"""
    """Inconsistent pressures: inlet pressure are equal to outlet pressure."""
    pump = Pump()
    enthalpy = MockEnthalpy()
    specific_volume = MockSpecificVolume()

    class InvalidInput:
      high_steam_level_pressure = 15  # bar
      condenser_operation_pressure = 35  # bar
      pump_efficiency = 85  # %

    input = InvalidInput()

    with pytest.raises(ThermodynamicError):
      pump.get_params_operation(input, enthalpy, specific_volume)