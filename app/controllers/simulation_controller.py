from ..services.full_cycles import FullCycle

def create_simulation(input, db):
  results = FullCycle.create_full_cycles_combined(input, db)
  return results
