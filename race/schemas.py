from typing import List, Optional
from pydantic import BaseModel


class ResponseStatus(BaseModel):
    success: bool
    status_code: int
    resposne: Optional[str] = None


class Car(BaseModel):
    car_name: str
    description: str
    color_name: List[str] 
    model_name: str


class UserCars(BaseModel):
    user_id: int
    username: str
    car: Optional[List[Car]] = []