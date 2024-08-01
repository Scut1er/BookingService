from datetime import date
from typing import Optional

from pydantic import BaseModel, model_validator
from sqlalchemy import JSON

from app.exceptions import IncorrectDateTo, TooLongPeriod


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: Optional[list[str]]
    rooms_quantity: int
    image_id: Optional[int]


class SGetHotels(SHotel):
    rooms_left: int


class SGetHotelsRequest(BaseModel):
    location: str
    date_from: date
    date_to: date

    @model_validator(mode="before")
    @classmethod
    def check_max_duration(cls, values):
        date_from = values.get("date_from")
        date_to = values.get("date_to")
        if date_from and date_to:
            if date_to <= date_from:
                raise IncorrectDateTo
            elif (date_to - date_from).days > 30:
                raise TooLongPeriod
        return values
