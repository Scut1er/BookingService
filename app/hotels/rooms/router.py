from datetime import date

from fastapi import APIRouter

from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRoom

router = APIRouter(
    prefix="/{hotel_id}/rooms",
)


@router.get("")
async def get_rooms(hotel_id: int, date_from: date, date_to: date) -> list[SRoom]:
    result = await RoomDAO.get_all(hotel_id, date_from, date_to)
    return result
