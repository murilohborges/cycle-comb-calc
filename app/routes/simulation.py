from fastapi import APIRouter
from ..models.input import Input
from ..models.output import Output
from ..controllers.simulation_controller import create_simulation

router = APIRouter()


@router.post("/simulation", tags=["Simulation"], response_model=Output)
async def call_simulation(input: Input):
  return create_simulation(input)
