from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.session import get_session
from ..models.input import Input
from ..models.output import Output
from ..controllers.simulation_controller import create_simulation

router = APIRouter()


@router.post(
  "/simulation", 
  tags=["Simulation"],
  summary="Run full thermodynamic simulation",
  description=(
    "This endpoint performs a complete thermodynamic analysis of the **Brayton** and **Rankine** cycles "
    "based on the input data provided in the request body. "
    "It calculates temperatures, pressures, efficiencies, and power outputs of the combined cycle system.\n\n"
    "### Notes:\n"
    "- All input parameters are required and validated according to predefined ranges.\n"
    "- The simulation assumes steady-state conditions.\n"
  ),
  response_description="Thermodynamic simulation results (Output model)",
  response_model=Output
  )
async def call_simulation(input: Input, db: Session = Depends(get_session)):
  return create_simulation(input, db)
