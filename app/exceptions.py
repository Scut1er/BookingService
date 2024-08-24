from typing import Optional

from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self, detail: Optional[str] = None):
        super().__init__(status_code=self.status_code,
                         detail=self.detail or self.detail)


class UserAlreadyExists(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


class IncorrectEmailOrPassword(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email Or password"


class TokenExpired(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token has expired"


class TokenAbsent(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token is absent"


class IncorrectTokenFormat(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect token format"


class UserIsNotPresent(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomsFullyBooked(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "No rooms left"


class RoomCannotBeBooked(BaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to book a room"


class CannotInsertData(BaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Cannot insert data into table"


class CannotAddBooking(BaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Cannot add booking"


class IncorrectDateTo(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Departure date must be at least 1 day later than arrival date"


class TooLongPeriod(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Booking cannot exceed 30 days"


class CannotDeleteData(BaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Cannot delete data from table"


class CannotDeleteBooking(BaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Cannot delete booking from table"


class CannotFetchBookings(BaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Cannot fetch bookings from table"


class IncorrectFormatFile(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "File must be a CSV"


class TableNotFound(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Table not found in the database"
