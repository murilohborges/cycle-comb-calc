from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Substance(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  name: str
  molar_mass: float
  lower_calorific_value: float
  created_at: datetime = Field(default_factory=datetime.utcnow)
  is_default: bool

class CorrelationSpecificHeat(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  substance_id: int = Field(default=None, foreign_key="substance.id")
  param_A: float
  param_B: float
  param_C: float
  param_D: float
  created_at: datetime = Field(default_factory=datetime.utcnow)
  is_default: bool