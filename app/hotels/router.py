from datetime import date

from fastapi import APIRouter

from app.hotels.dao import HotelDAO
from app.hotels.schemas import SGetHotels, SGetHotelsRequest, SHotel

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.get("")
async def get_hotels(location: str, date_from: date, date_to: date) -> list[SGetHotels]:
    hotels_request = SGetHotelsRequest(location=location, date_from=date_from, date_to=date_to)
    result = await HotelDAO.get_all(hotels_request.location,
                                    hotels_request.date_from,
                                    hotels_request.date_to)
    return result


@router.get("/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> SHotel:
    result = await HotelDAO.get_by_id(hotel_id)
    return result
