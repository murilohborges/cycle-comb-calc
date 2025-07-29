from fastapi import FastAPI
from ..models.substance import Substance
from typing import List

router = APIRouter()


@router.get("/substances", tags=["Substances"], response_model=List[Substance])
async def show_substances():
  return Substance(
    name="methane",
    formula="CH4",
    cas_number="74-82-8"
  )
