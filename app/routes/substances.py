from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database.session import get_session
from app.models.substance import Substance
from app.controllers.substances_controller import get_all_substances
from typing import List

router = APIRouter()


@router.get("/substances", tags=["Substances"], response_model=List[Substance])
async def show_substances(db: Session = Depends(get_session)):
  return get_all_substances(db)
