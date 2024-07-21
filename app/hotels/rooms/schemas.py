from typing import Optional

from pydantic import BaseModel


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str]
    price: int
    services: Optional[list[str]]
    quantity: int
    image_id: Optional[int]
    total_cost: int
    rooms_left: int
