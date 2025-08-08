import pytest
from app.controllers.substances_controller import get_all_substances
from app.database.models import Substance

def test_get_all_substances_returns_data(mocker):
  """
  Testing substances controller with a mock
  """
  # Mock with substances for the test
  mock_substances = [
      Substance(name="water", formula="H2O", cas_number="7732-18-5"),
      Substance(name="sodium", formula="Na", cas_number="7440-23-5"),
    ]

  # Create session's mock
  mock_session = mocker.MagicMock()

  # Create a mock to the result of session.exec()
  mock_result = mocker.MagicMock()

  # Set the return of all() method
  mock_result.all.return_value = mock_substances

  # Causes session.exec(...) to return this mock
  mock_session.exec.return_value = mock_result

  # Run the function with the mocked session
  result = get_all_substances(mock_session)

  # Checks if the result matches what was expected
  assert result == mock_substances
  assert len(result) > 0
  assert mock_session.exec.called
  assert mock_result.all.called
