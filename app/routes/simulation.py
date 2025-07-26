from fastapi import APIRouter
from ..models.input import Input

router = APIRouter()


@router.get("/simulation", tags=["Simulation"])
async def create_simulation(input: Input):
    return {"message testing"}
