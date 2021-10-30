from typing import Optional
from pydantic import BaseModel, Field


class Token(BaseModel):
    auth_token: str = Field(..., description="Токен")
    type_token: str = Field(..., description="Тип токена")


class User(BaseModel):
    user_id: int
    username: str
    role_id: int
    email: Optional[str] = None
    first_name: Optional[str] = None
    second_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


class CreateUser(BaseModel):
    first_name: str = Field(None, description="Имя пользователя")
    second_name: str = Field(None, description="Фамилия пользователя")
    username: str = Field(None, description="Логин пользователя")
    password: str = Field(None, description="Пароль пользователя")
    email: Optional[str] = Field(None, description="email")


class UpdatedUser(BaseModel):
    user_id: int = Field(
        None,
        description="Id пользователя",
    )
    first_name: Optional[str] = Field(None, description="Имя пользователя")
    second_name: Optional[str] = Field(
        None, description="Фамилия пользователя"
    )
    email: Optional[str] = Field(None, description="Email")
    password: Optional[str] = Field(None, description="Пароль пользователя")


class ResponseUser(BaseModel):
    status_code: int = Field(None, description="Статус ответа пользователю")
    description: str = Field(None, description="Описание ответа пользователю")


class UserLogin(BaseModel):
    username: str
    password: str