from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .errors import (
  ThermodynamicError,
  LogicConstraintError,
  DataValidationError,
  NotFoundError,
  ComputationalError
)

def register_error_handlers(app):
  """Attach custom error handlers to the FastAPI application instance."""

  @app.exception_handler(ThermodynamicError)
  async def thermodynamic_error_handler(request: Request, exc: ThermodynamicError):
    # Physical law or thermodynamic principle violation
    return JSONResponse(
      status_code=422,
      content={"error": str(exc), "type": "ThermodynamicError"}
    )

  @app.exception_handler(LogicConstraintError)
  async def logic_constraint_error_handler(request: Request, exc: LogicConstraintError):
    # Logical or business rule violation
    return JSONResponse(
      status_code=400,
      content={"error": str(exc), "type": "LogicConstraintError"}
    )

  @app.exception_handler(DataValidationError)
  async def data_validation_error_handler(request: Request, exc: DataValidationError):
    # Invalid or inconsistent input data
    return JSONResponse(
      status_code=422,
      content={"error": str(exc), "type": "DataValidationError"}
    )

  @app.exception_handler(NotFoundError)
  async def not_found_error_handler(request: Request, exc: NotFoundError):
    # Database entity or parameter not found
    return JSONResponse(
      status_code=404,
      content={"error": str(exc), "type": "NotFoundError"}
    )

  @app.exception_handler(ComputationalError)
  async def computational_error_handler(request: Request, exc: ComputationalError):
    # Convergence or numerical instability in calculation
    return JSONResponse(
      status_code=500,
      content={"error": str(exc), "type": "ComputationalError"}
    )

  @app.exception_handler(RequestValidationError)
  async def validation_error_handler(request: Request, exc: RequestValidationError):
    # Extract details of each validation error
    errors = [{"loc": e["loc"], "msg": e["msg"], "type": e["type"]} for e in exc.errors()]
    return JSONResponse(
      status_code=422,
      content={
        "error": "Input validation failed",
        "type": "RequestValidationError",
        "details": errors
      }
    )

  @app.exception_handler(Exception)
  async def generic_error_handler(request: Request, exc: Exception):
    # Unexpected or unhandled exception
    return JSONResponse(
      status_code=500,
      content={"error": str(exc), "type": "InternalServerError"}
    )
