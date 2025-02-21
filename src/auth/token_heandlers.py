import uuid
from datetime import timedelta
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi import Request

from src.auth.enums import Rights
from src.auth.exceptions import refresh_token_exception, access_token_exception, logout_exception
from src.auth.crypto_heandlers import decode_jwt, sign_jwt
from src.auth.redis_connection import redis_client
from src.auth.service import UserService


def get_current_user(request: Request):

    token = request.headers.get("Authorization")


    if not token:
        id_from_refresh_token = int(do_refresh_token(request))
        if not id_from_refresh_token:
            raise refresh_token_exception

        return id_from_refresh_token

    id_from_access_token = decode_jwt(token).get("user_id")

    if id_from_access_token is None:
        id_from_refresh_token = do_refresh_token(request)
        if id_from_refresh_token is None:
            raise access_token_exception

    return id_from_access_token


def do_refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise refresh_token_exception

    id: int = redis_client.get(refresh_token)
    if not id:
        raise refresh_token_exception

    access_token = sign_jwt(id)
    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(key="access_token", value=access_token, httponly=True)

    return id


def create_refresh_token(id: int):
    """Генерация refresh токена"""
    refresh_token = str(uuid.uuid4())

    # Сохранение токена в Redis
    redis_client.setex(refresh_token, timedelta(days=7), id)

    return refresh_token


def delete_refresh_token(request: Request) -> dict | HTTPException:
    """Удаление refresh токена"""

    try:
        refresh_token = request.cookies.get("refresh_token")

        redis_client.delete(refresh_token)

    except logout_exception as e:

        raise logout_exception

    return {"status": "logout"}






