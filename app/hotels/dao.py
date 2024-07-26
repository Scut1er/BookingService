from datetime import date

from sqlalchemy import select, func

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @staticmethod
    async def get_all(location: str, date_from: date, date_to: date):
        date_conditions = BaseDAO.create_date_conditions(date_from, date_to)
        booked_rooms_subquery = BaseDAO.create_booked_rooms_subquery(date_conditions)

        query = (
            select(
                Hotels.id.label('id'),
                Hotels.name.label('name'),
                Hotels.location.label('location'),
                Hotels.services.label('services'),
                Hotels.rooms_quantity.label('rooms_quantity'),
                Hotels.image_id.label('image_id'),
                (Hotels.rooms_quantity - func.coalesce(func.sum(booked_rooms_subquery.c.booked_rooms), 0)).label(
                    'rooms_left')
            )
            .select_from(Hotels)
            .join(Rooms, Rooms.hotel_id == Hotels.id)
            .outerjoin(booked_rooms_subquery, booked_rooms_subquery.c.hotel_id == Hotels.id)
            .where(
                Hotels.location.like(f'%{location}%'))
            .group_by(
                Hotels.id,
            )
            .having(
                (Hotels.rooms_quantity - func.coalesce(func.sum(booked_rooms_subquery.c.booked_rooms), 0)) > 0
            )
            .distinct(Hotels.id)
        )
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.mappings().all()
