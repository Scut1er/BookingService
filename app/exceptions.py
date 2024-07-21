from typing import Optional

from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self, detail: Optional[str] = None):
        super().__init__(status_code=self.status_code, detail=self.detail or self.detail)


class UserAlreadyExists(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


class IncorrectEmailOrPassword(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email Or password"


class TokenExpired(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token has expired"


class TokenAbsent(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token is absent"


class IncorrectTokenFormat(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect token format"


class UserIsNotPresent(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomsFullyBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"


class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось забронировать номер ввиду неизвестной ошибки"


class CannotInsertData(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Cannot insert data into table"


class CannotAddBooking(CannotInsertData):
    detail = "Cannot add booking"


class CannotDeleteData(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Cannot delete data from table"


class CannotDeleteBooking(CannotDeleteData):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Cannot delete booking from table"


class CannotFetchBookings(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Cannot fetch bookings from table"
