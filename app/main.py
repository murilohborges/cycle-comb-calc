from fastapi import FastAPI
from pydantic import BaseModel
from .routes import simulation, substances
from typing import List
import logging

# Show only SQLAlchemy warnings and errors
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)

app = FastAPI(
  title="Simulator for combined thermodynamic cycles (Brayton-Rankine)")
app.include_router(simulation.router)
app.include_router(substances.router)


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
