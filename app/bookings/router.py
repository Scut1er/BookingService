from fastapi import APIRouter, Depends
from pydantic import TypeAdapter
from fastapi_versioning import version

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SAddBookingRequest, SGetBooking, SNewBooking
from app.exceptions import CannotDeleteBooking, RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/booking",
    tags=["Bookings"],
)


@router.post("")
async def add_booking(
    booking_request: SAddBookingRequest, user: Users = Depends(get_current_user)
) -> SNewBooking:
    booking = await BookingDAO.add(
        user.id,
        booking_request.room_id,
        booking_request.date_from,
        booking_request.date_to,
    )
    if not booking:
        raise RoomCannotBeBooked
    booking = TypeAdapter(SNewBooking).validate_python(booking).model_dump()
    send_booking_confirmation_email.delay(booking, user.email)
    return booking


@router.get("/my_bookings")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SGetBooking]:
    result = await BookingDAO.get_all_bookings(user_id=user.id)
    return result


@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.get_one_or_none(user_id=user.id, id=booking_id)
    if booking:
        return await BookingDAO.delete_by_id(booking_id)
    else:
        raise CannotDeleteBooking
