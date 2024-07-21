from typing import Optional

from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    location: Mapped[str]
    services: Mapped[Optional[list[str]]] = mapped_column(JSON)
    rooms_quantity: Mapped[int]
    image_id: Mapped[Optional[int]]
