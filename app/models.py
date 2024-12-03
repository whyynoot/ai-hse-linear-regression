from pydantic import BaseModel
from typing import List, Union, Optional

class Item(BaseModel):
    name: str
    year: int
    km_driven: int
    fuel: str
    seller_type: str
    transmission: str
    owner: str
    mileage: str
    engine: str
    max_power: str
    torque: str
    seats: float


class Items(BaseModel):
    objects: List[Item]

class PredictionSuccessResponse(BaseModel):
    success: bool = True
    predictions: Optional[List[float]]

class PredictionErrorResponse(BaseModel):
    success: bool = False
    error: str


PredictionResponse = Union[PredictionSuccessResponse, PredictionErrorResponse]