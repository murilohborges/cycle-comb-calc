from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.session import get_session
from app.models.substance import Substance
from app.controllers.substances_controller import get_all_substances
from typing import List

router = APIRouter()


@router.get(
  "/substances", 
  tags=["Substances"],
  summary="Retrieve all registered substances",
  description=(
    "This endpoint returns a list of all chemical substances stored in the database. "
    "Each substance includes its thermodynamic and physical properties used in the simulation processes.\n\n"
    "### Notes:\n"
    "- The data is read directly from the system database.\n"
    "- Each record includes information such as name, molecular weight, and specific heat.\n"
    "- The endpoint does not require any parameters."
  ),
  response_description="List of substances with their respective properties",
  response_model=List[Substance])
async def show_substances(db: Session = Depends(get_session)):
  return get_all_substances(db)
