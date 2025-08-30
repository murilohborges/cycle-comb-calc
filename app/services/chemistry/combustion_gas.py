class CombustionGas:
  """
  Service class to calculate input air's properties.
  """
  def __init__(self, input_data, substance_repository):
    self.input = input_data
  
  def fraction_molar_calc(self, flows):
    """
    Calculation of molar fractions of input air.
    """
    total_flow = sum(flows.values())

    fractions = {
        name: flow / total_flow
        for name, flow in flows.items()
      }
    return fractions