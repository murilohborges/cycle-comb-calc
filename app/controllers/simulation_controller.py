from ..services.orchestrators.full_cycles import FullCycles
from ..repositories.repositories_container import RepositoriesContainer

def create_simulation(input, db):
  repos = RepositoriesContainer(db)
  full_cycles = FullCycles(input, repos)
  results = full_cycles.create_full_cycles_combined()
  return results
