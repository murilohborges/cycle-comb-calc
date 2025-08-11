import pytest
from app.controllers.simulation_controller import create_simulation

def test_create_simulation_returns_result():
  """
  Testing simulation controller returns a result not null
  """
  result = create_simulation(input)

  print(result)
  assert len(result) == 0