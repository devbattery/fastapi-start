from fastapi import APIRouter
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette import status

from TodoApp.models import Users

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class CreateUserRequest(BaseModel):
    nickname: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


@router.post("/api/auth", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        nickname=create_user_request.nickname,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    return create_user_model
