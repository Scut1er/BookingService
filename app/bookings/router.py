from datetime import date

from fastapi import APIRouter, Depends

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SGetBooking
from app.exceptions import RoomCannotBeBooked, CannotDeleteBooking
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SGetBooking]:
    result = await BookingDAO.get_all_bookings(user_id=user.id)
    return result


@router.post("")
async def add_booking(room_id: int, date_from: date, date_to: date,
                      user: Users = Depends(get_current_user)) -> SBooking:
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    return booking


@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.get_one_or_none(user_id=user.id, id=booking_id)
    if booking:
        return await BookingDAO.delete_by_id(booking_id)
    else:
        raise CannotDeleteBooking