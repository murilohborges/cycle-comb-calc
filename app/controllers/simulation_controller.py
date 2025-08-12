from ..services.full_cycles import FullCycles

def create_simulation(input, db):
  full_cycles = FullCycles(input, db)
  results = full_cycles.create_full_cycles_combined()
  return results
