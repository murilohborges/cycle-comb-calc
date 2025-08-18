from .substance_repository import SubstanceRepository

class RepositoriesContainer:
  def __init__(self, db):
    self.substance_repository = SubstanceRepository(db)
