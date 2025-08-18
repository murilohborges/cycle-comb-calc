import pytest
from app.controllers.simulation_controller import create_simulation
from tests.conftest import MockDB

def test_create_simulation_calls_full_cycles(mocker, fake_input, fake_db):
    """
    Tests whether the controller correctly instantiates FullCycles,
    calls the create_full_cycles_combined method, and returns the result.
    """
    # Mock of the instance that will be returned by the FullCycles class
    mock_full_cycles_instance = mocker.Mock()
    mock_full_cycles_instance.create_full_cycles_combined.return_value = {"status": "ok"}
    
    # Patch of the FullCycles class in the controller module
    mock_full_cycles_class = mocker.patch(
        "app.controllers.simulation_controller.FullCycles",
        return_value=mock_full_cycles_instance
    )

    # Calling the function to be tested
    result = create_simulation(fake_input, fake_db)

    # Checks if the FullCylces class was instantiated with the correct arguments
    mock_full_cycles_class.assert_called_once()
    # Checks if the method was called exactly once
    mock_full_cycles_instance.create_full_cycles_combined.assert_called_once()
    # Checks if the controller return is the method return
    assert result == {"status": "ok"}