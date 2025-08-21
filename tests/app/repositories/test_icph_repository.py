import pytest
from sqlmodel import SQLModel, Session, create_engine
from app.database.models import CorrelationSpecificHeat
from app.repositories.icph_repository import ICPHRepository

@pytest.fixture
def db_session():
  engine = create_engine("sqlite:///:memory:")
  SQLModel.metadata.create_all(engine)
  with Session(engine) as session:
    # Inserting fictitious data
    session.add_all([
      CorrelationSpecificHeat(
        substance_id=1,
        param_A=1,
        param_B=2,
        param_C=3,
        param_D=4,
        is_default=1
      ),
      CorrelationSpecificHeat(
        substance_id=2,
        param_A=3,
        param_B=6,
        param_C=9,
        param_D=12,
        is_default=1
      )
    ])
    session.commit()
    yield session
  
def test_get_by_substance_id(db_session):
  """
  Testing get_by_substance_id method from ICPHRepository
  """
  repo = ICPHRepository(db_session)
  substance_id = 1
  result = repo.get_by_substance_id(substance_id)
  assert len(result) == 4
  assert result == ({"param_A": 1, "param_B": 2,"param_C": 3,"param_D": 4})