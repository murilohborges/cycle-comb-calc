class ThermodynamicError(Exception):
  """Raised when a thermodynamic law or principle is violated."""
  pass


class LogicConstraintError(Exception):
  """Raised when logical or business constraints are not respected."""
  pass


class DataValidationError(Exception):
  """Raised when input data does not match expected format or physical limits."""
  pass


class NotFoundError(Exception):
  """Raised when a required record or parameter is missing in the database."""
  pass


class ComputationalError(Exception):
  """Raised when a numerical method or iterative algorithm fails to converge."""
  pass
