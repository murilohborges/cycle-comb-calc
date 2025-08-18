from app.repositories.repositories_container import RepositoriesContainer
from app.repositories.substance_repository import SubstanceRepository

class MockDB:
  pass

def test_repositories_container_instantiation():
    mock_db = MockDB()
    container = RepositoriesContainer(mock_db)

    # Checks if the attribute is of the correct type
    assert isinstance(container.substance_repository, SubstanceRepository)
