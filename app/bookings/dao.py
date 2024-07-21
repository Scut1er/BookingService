from datetime import date

from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import CannotAddBooking, CannotFetchBookings, RoomsFullyBooked
from app.hotels.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        try:
            date_conditions = BaseDAO.create_date_conditions(date_from, date_to)
            booked_rooms_subquery = BaseDAO.create_booked_rooms_subquery(date_conditions)
            query = (
                select(
                    (Rooms.quantity - func.coalesce(booked_rooms_subquery.c.booked_rooms, 0)).label('available_rooms')
                )
                .select_from(Rooms)
                .outerjoin(booked_rooms_subquery, booked_rooms_subquery.c.room_id == Rooms.id)
                .where(Rooms.id == room_id)
            )
            async with async_session_maker() as session:
                result = await session.execute(query)
                available_rooms = result.scalar()

                if available_rooms == 0:
                    raise RoomsFullyBooked

                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.scalar(get_price)

            return await super().add(user_id=user_id, room_id=room_id, date_from=date_from, date_to=date_to,
                                     price=price)

        except SQLAlchemyError or Exception:
            raise CannotAddBooking

    @staticmethod
    async def get_all_bookings(user_id: int):
        try:
            query = (
                select(
                    Bookings.id.label('id'),
                    Bookings.room_id.label('room_id'),
                    Bookings.date_from.label('date_from'),
                    Bookings.date_to.label('date_to'),
                    Bookings.user_id.label('user_id'),
                    Bookings.price.label('price'),
                    Bookings.total_cost.label('total_cost'),
                    Bookings.total_days.label('total_days'),
                    Rooms.image_id.label('image_id'),
                    Rooms.name.label('name'),
                    Rooms.description.label('description'),
                    Rooms.services.label('services')
                )
                .join(Rooms, Bookings.room_id == Rooms.id)
                .where(Bookings.user_id == user_id)
                .order_by(Bookings.date_from, Bookings.id)
            )
            async with async_session_maker() as session:
                results = await session.execute(query)
                return results.mappings().all()
        except SQLAlchemyError or Exception:
            raise CannotFetchBookings
