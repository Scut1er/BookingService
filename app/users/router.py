from fastapi import APIRouter, Response, Depends

from app.exceptions import UserAlreadyExists, IncorrectEmailOrPassword
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth, SGetUser
from app.users.dao import UserDAO

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

router_users = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router_auth.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UserDAO.get_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExists
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)


@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPassword
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router_auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router_users.get("/me")
async def read_user_me(current_user: Users = Depends(get_current_user)) -> SGetUser:
    return await UserDAO.get_by_id(current_user.id)
