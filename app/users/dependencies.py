from fastapi import Request, Depends
from jose import jwt, JWTError, ExpiredSignatureError

from app.config import settings
from app.exceptions import TokenExpired, IncorrectTokenFormat, TokenAbsent, UserIsNotPresent
from app.users.dao import UserDAO


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsent
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except ExpiredSignatureError:
        raise TokenExpired
    except JWTError:
        raise IncorrectTokenFormat
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresent
    user = await UserDAO.get_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresent
    return user
