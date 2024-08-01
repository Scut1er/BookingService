from datetime import date
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator

from app.exceptions import IncorrectDateTo, TooLongPeriod


class SAddBookingRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date



    @model_validator(mode="before")
    @classmethod
    def check_max_duration(cls, values):
        date_from = date.fromisoformat(values.get("date_from"))
        date_to = date.fromisoformat(values.get("date_to"))
        if date_from and date_to:
            if date_to <= date_from:
                raise IncorrectDateTo
            elif (date_to - date_from).days > 30:
                raise TooLongPeriod
        return values


class SBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int


class SNewBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class SGetBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    image_id: int
    name: str
    description: Optional[str]
    services: Optional[list[str]]
