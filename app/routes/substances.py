from fastapi import APIRouter
from app.models.substance import Substance
from app.controllers.substances_controller import get_all_substances
from typing import List

router = APIRouter()


@router.get("/substances", tags=["Substances"], response_model=List[Substance])
async def show_substances():
  return get_all_substances()
