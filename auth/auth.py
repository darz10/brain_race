import datetime
from typing import Optional

from fastapi import APIRouter, Request, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security.oauth2 import SecurityScopes
from pydantic import ValidationError
from jose import jwt, JWTError
from auth.get_hash_password import (
    verify_password,
)
from auth.schemas import Token, UserInDB
from settings import settings
import db


router = APIRouter()

ACCESS_TOKEN_EXPIRE_DAYS = 365 * 5
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login")


""" curl -X POST http://127.0.0.1:8000/v1/login -F "username=testadmin" -F "password=qwerty12345" """


@router.post("/v1/login")
async def get_auth_data(
    request: Request,
    response: Response,
    user_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    user = await auth_user(user_data.username, user_data.password)
    return await login(user, settings, response)


async def get_user(username: str) -> UserInDB:
    user_data = await db.get_user(username)
    if user_data:
        return UserInDB(
            username=username,
            user_id=user_data["user_id"],
            first_name=user_data["first_name"],
            second_name=user_data["second_name"],
            hashed_password=user_data["hashed_password"],
            email=user_data["email"],
            role_id=user_data["role_id"],
            disabled=user_data["disabled"],
        )


async def auth_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_token(
    data: dict,
    secret_key: str,
    expires_delta: Optional[datetime.timedelta] = None,
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + datetime.timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


async def login(user, response):
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_token(
        data={"sub": user.username, "user_id": user.user_id},
        expires_delta=access_token_expires,
        secret_key=SECRET_KEY,
    )
    resp = {"access_token": access_token, "token_type": "bearer"}
    response.headers["authorization"] = access_token

    return resp


async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    settings=settings,
) -> UserInDB:
    if security_scopes.scopes:
        auth_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        auth_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": auth_value},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except (ValidationError, JWTError):
        raise credentials_exception

    user = await db.get_user(username=username)

    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in user.scopes:
            raise HTTPException(
                status_code=403,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": auth_value},
            )
    return user
