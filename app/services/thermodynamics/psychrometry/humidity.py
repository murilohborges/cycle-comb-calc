class Humidity:
  """
  Service class to calculate absolute humidity of the air.
  """
  def absolute_humidity(saturation_pressure, local_atmospheric_pressure, relative_humidity):
    """
    Calculation of absolute humidity in kg of water/kg of dried air
    """
    steam_pressure = saturation_pressure*relative_humidity

    # Converting local_atmospheric_pressure from atm to bar
    local_atmospheric_pressure = local_atmospheric_pressure * (1.01325)

    result = 0.622 * (steam_pressure/(local_atmospheric_pressure-steam_pressure))
    return result