import pytest

# Mock to simulate the database
class MockDB:
  def __init__(self, results):
    self._results = results

  def exec(self, statement):
    return self

  def all(self):
    return self._results


# Mock to simulate the service's input
class MockInput:
  def __init__(self, **kwargs):
    for k, v in kwargs.items():
      setattr(self, k, v)


@pytest.fixture
def mock_db_factory():
    """
    Fixture that returns a factory to create mock of DB
    with simulate results (LHV, molar_mass)
    """
    def _factory(results):
        return MockDB(results)
    return _factory


@pytest.fixture
def mock_input_factory():
    """
    Fixture that returns a factory to create input mocks
    with arbitrary attributes.
    """
    def _factory(**kwargs):
        return MockInput(**kwargs)
    return _factory


# Global Fixtures for Controller
@pytest.fixture
def fake_input():
    """
    Generic input for controllers
    """
    return {"some": "data"}

@pytest.fixture
def fake_db():
    """
    Generic DB for controllers
    """
    return "fake_db"