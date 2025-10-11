from app.utils.errors import ComputationalError

class SecantMethod():
  """Service class to calculate the computational routine of iteration by the Secant method.
  Utilized for the calculation of outlet temperature in isenthalpic and isentropic process"""
  def run(self, inlet_property, thermo_property_function, outlet_pressure, saturation_parameters):
    """Calculation of the root of function"""
    maximum_iterations = 100
    i = 0
    tolerance = 1

    # Estimating initial values ​​by values ​​close to the saturation temperature at the outlet pressure
    outlet_saturation_temperature = saturation_parameters.saturation_temperature(outlet_pressure)
    T0n = outlet_saturation_temperature + 0.01
    Tn = outlet_saturation_temperature + 0.02

    while tolerance > 0.01 and i < maximum_iterations:

      # Calculating difference between inlet entropy (constant) and outlet entropy (iteration value) that must be zero (isentropic process)
      difference_Tn = abs(inlet_property - thermo_property_function.overheated_steam(outlet_pressure, Tn))
      difference_T0n = abs(inlet_property - thermo_property_function.overheated_steam(outlet_pressure, T0n))

      # Avoid division by zero if differences are equal
      if difference_Tn == difference_T0n:
        raise ComputationalError("Secant method failed: no variation between iterations (possible flat function)")

      # Calculation of the iteration
      T2n = Tn - difference_Tn * ((Tn - T0n) / (difference_Tn - difference_T0n))

      # Updating tolerance value after the iteration for the checking 'ending condition'
      tolerance = abs(difference_Tn)

      # Updating values for the next necessary iteration
      T0n = Tn
      Tn = T2n
      i = i + 1

    if i >= maximum_iterations:
      raise ComputationalError("Secant method did not converge after maximum iterations")

    return T2n
