from fastapi import FastAPI, Request
from pydantic import BaseModel
from .routes import simulation, substances
from typing import List
from app.utils.error_handler import register_error_handlers
import logging
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

# Show only SQLAlchemy warnings and errors
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
  title="Simulator for combined thermodynamic cycles (Brayton-Rankine)")
app.include_router(simulation.router)
app.include_router(substances.router)
register_error_handlers(app)

app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Too many requests — please wait a moment before trying again."
        },
    )


@app.middleware("http")
async def global_rate_limit(request: Request, call_next):
    response = await limiter.limit("20/minute")(call_next)(request)
    return response

origins = [
  "http://localhost:5173",
  "https://cycle-comb-calc.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
