from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.session import get_session
from ..models.input import Input
from ..models.output import Output
from ..controllers.simulation_controller import create_simulation

router = APIRouter()


@router.post("/simulation", tags=["Simulation"], response_model=Output)
async def call_simulation(input: Input, db: Session = Depends(get_session)):
  return create_simulation(input, db)
