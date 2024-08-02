from typing import Optional

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]
    services: Mapped[Optional[list[str]]] = mapped_column(JSON)
    quantity: Mapped[int]
    image_id: Mapped[Optional[int]]

    hotel: Mapped["Hotels"] = relationship(back_populates="rooms")
    bookings: Mapped[list["Bookings"]] = relationship(back_populates="room")

    def __str__(self):
        return f"Room: {self.name}"
