from datetime import date

from sqlalchemy import or_, and_, select, func

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms


class RoomDAO(BaseDAO):
    model = Rooms

    @staticmethod
    async def get_all(hotel_id: int, date_from: date, date_to: date):
        date_conditions = BaseDAO.create_date_conditions(date_from, date_to)
        booked_rooms_subquery = BaseDAO.create_booked_rooms_subquery(date_conditions)

        query = (
            select(
                Rooms.id.label('id'),
                Rooms.hotel_id.label('hotel_id'),
                Rooms.name.label('name'),
                Rooms.description.label('description'),
                Rooms.services.label('services'),
                Rooms.price.label('price'),
                Rooms.quantity.label('quantity'),
                Rooms.image_id.label('image_id'),
                (Rooms.quantity - func.coalesce(booked_rooms_subquery.c.booked_rooms, 0)).label('rooms_left'),
                (Rooms.price * (date_to - date_from).days).label('total_cost')
            )
            .select_from(Rooms)
            .outerjoin(booked_rooms_subquery, booked_rooms_subquery.c.room_id == Rooms.id)
            .where(Rooms.hotel_id == hotel_id)
        )
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.mappings().all()
