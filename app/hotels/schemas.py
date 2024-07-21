from datetime import date
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import JSON


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: Optional[list[str]]
    rooms_quantity: int
    image_id: Optional[int]


class SGetHotels(SHotel):
    rooms_left: int
