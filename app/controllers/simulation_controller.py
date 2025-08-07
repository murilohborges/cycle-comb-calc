from ..services.full_cycles import FullCycle

def create_simulation(input):
  results = FullCycle.create_full_cycles_combined()
  return results
