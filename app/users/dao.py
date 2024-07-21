from sqlalchemy import select

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.users.models import Users


class UserDAO(BaseDAO):
    model = Users

    @classmethod
    async def get_by_id(cls, model_id: int):
        query = (select(
            Users.id.label('id'),
            Users.email.label('email')
            )
            .filter_by(id=model_id))
        async with async_session_maker() as session:
            result = await session.execute(query)
            return result.mappings().one_or_none()
