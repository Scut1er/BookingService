from datetime import date

from sqlalchemy import select, insert, delete, or_, and_, func

from app.bookings.models import Bookings
from app.database import async_session_maker
from app.exceptions import CannotInsertData, CannotDeleteData
from app.hotels.rooms.models import Rooms


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, **data):
        try:
            query = insert(cls.model).values(**data).returning(cls.model.__table__.columns)
            async with async_session_maker() as session:
                insert_data = await session.execute(query)
                await session.commit()
                return insert_data.mappings().one()
        except Exception:
            raise CannotInsertData

    @classmethod
    async def delete_by_id(cls, model_id: int):
        try:
            query = delete(cls.model).where(cls.model.id == model_id)
            async with async_session_maker() as session:
                await session.execute(query)
                await session.commit()
        except Exception as e:
            print(e)
            raise CannotDeleteData

    @classmethod
    async def get_by_id(cls, model_id: int):
        query = select(cls.model.__table__.columns).filter_by(id=model_id)
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        query = select(cls.model.__table__.columns).filter_by(**filter_by)
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @staticmethod
    def create_date_conditions(date_from: date, date_to: date):
        return or_(
            and_(Bookings.date_from >= date_from, Bookings.date_from <= date_to),
            and_(Bookings.date_from <= date_from, Bookings.date_to > date_from),
            and_(Bookings.date_from <= date_from, Bookings.date_to >= date_to)
        )

    @staticmethod
    def create_booked_rooms_subquery(date_conditions):
        return (
            select(
                Rooms.hotel_id,
                Rooms.id.label('room_id'),
                func.count(Bookings.id).label('booked_rooms')
            )
            .join(Bookings, Bookings.room_id == Rooms.id)
            .filter(date_conditions)
            .group_by(Rooms.hotel_id, Rooms.id)
            .subquery()
        )