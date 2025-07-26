from fastapi import FastAPI
from pydantic import BaseModel
from .routes import simulation
from typing import List

app = FastAPI(
    title="Simulator for combined thermodynamic cycles (Brayton-Rankine)")
app.include_router(simulation.router)


class InfoResponse(BaseModel):
    message: str
    description: str
    available_endpoints: List[str]
    documentation: str


@app.get("/", response_model=InfoResponse, tags=["Root"])
async def read_root():
    return InfoResponse(
        message="Welcome to the Combined Thermodynamic Cycles Calculations API!",
        description="Microservice for combined thermodynamic cycles calculations.",
        available_endpoints=["POST /simulation", "GET /substances"],
        documentation="/docs"
    )
