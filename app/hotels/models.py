from typing import Optional

from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    location: Mapped[str]
    services: Mapped[Optional[list[str]]] = mapped_column(JSON)
    rooms_quantity: Mapped[int]
    image_id: Mapped[Optional[int]]

    rooms: Mapped[list["Rooms"]] = relationship(back_populates="hotel")

    def __str__(self):
        return f"Hotel: {self.name}, location: {self.location}"
