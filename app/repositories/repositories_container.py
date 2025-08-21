from .substance_repository import SubstanceRepository
from .icph_repository import ICPHRepository

class RepositoriesContainer:
  def __init__(self, db):
    self.substance_repository = SubstanceRepository(db)
    self.icph_repository = ICPHRepository(db)
    
