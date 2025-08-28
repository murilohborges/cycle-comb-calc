import pytest
from sqlmodel import SQLModel, Session, create_engine
from app.database.models import Substance
from app.repositories.substance_repository import SubstanceRepository

@pytest.fixture
def db_session():
  engine = create_engine("sqlite:///:memory:")
  SQLModel.metadata.create_all(engine)
  with Session(engine) as session:
    # Inserting fictitious data
    session.add_all([
      Substance(name="hydrogen", molar_mass=0.016, lower_calorific_value=50000, formula="H2", cas_number="1333-74-0", is_default=1),
      Substance(name="methane", molar_mass=0.014, lower_calorific_value=45000, formula="CH4", cas_number="74-82-8", is_default=1)
    ])
    session.commit()
    yield session

def test_get_all(db_session):
  """
  Testing get_all() method from SubstanceRepository
  """
  repo = SubstanceRepository(db_session)
  results = repo.get_all()
  assert len(results) == 2
  assert results["hydrogen"] == ({'id': 1, 'molar_mass': 0.016, 'lower_calorific_value': 50000, 'formula': "H2"})
  assert results["methane"] == ({'id': 2, 'molar_mass': 0.014, 'lower_calorific_value': 45000, 'formula': "CH4"})
