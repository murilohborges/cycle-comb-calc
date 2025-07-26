from pydantic import BaseModel


class Substance(BaseModel):
    """
    All substances available to the simulation
    """
    id: int
    name: str
    formula: str
    cas_number: str
