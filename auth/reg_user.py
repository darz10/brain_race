from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from auth.get_hash_password import get_password_hash
from auth.auth import get_current_user
from auth.schemas import CreateUser, ResponseUser, UpdatedUser, User
from settings import settings
from db import BrainRaceDB


router = APIRouter()


@router.post("/v1/create-user")
async def add_new_user(request: Request, user: CreateUser):
    """Создание нового пользователя"""
    try:
        # //TODO создать проверку на максимальное создание аккаунтов 5 шт.
        await BrainRaceDB.add_new_user(
            user.username,
            user.first_name,
            user.second_name,
            get_password_hash(user.password),
            user.email,
        )
        return JSONResponse(status_code=201)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


@router.post("/v1/update-user")
async def update_user(
    request: Request,
    user: UpdatedUser,
    current_user: User = Depends(get_current_user),
):
    """Изменение информации о пользователе
    curl -X POST http://127.0.0.1:8000/v1/update_user -H '{"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0YWRtaW4iLCJ1c2VyX2lkIjoxLCJleHAiOjE3OTE3NzQ3MzR9.-CH0HOoZxmUPCGUfHxG1SxHtk7WyrPdElShoobQwguE"}' -d '{"user_id": 2, "first_name": "Kirill", "email": "qwerty@qwe.ru"}'"""
    try:
        await BrainRaceDB.update_user(
            user.user_id,
            user.first_name,
            user.second_name,
            user.username,
            user.password,
            user.email,
        )
        return ResponseUser(
            status_code=200, description="Данные успешно изменены"
        )
    except Exception as e:
        print(e)
