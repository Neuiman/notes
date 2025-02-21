from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.auth.crypto_heandlers import sign_jwt
from src.auth.schemas import UserLoginSchema, UserRegisterSchema
from src.auth.service import UserService
from src.auth.token_heandlers import create_refresh_token, delete_refresh_token

router = APIRouter()

@router.post("/login")
async def user_login(user: UserLoginSchema, user_service: UserService):

    if await user_service.verify_user(user):
        id = await user_service.get_id(user.email)
        access_token = sign_jwt(id)
        refresh_token = create_refresh_token(id)
        response = JSONResponse(content={"token": access_token, "refresh_token": refresh_token, "token_type": "bearer"})
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
        response.set_cookie(key="access_token", value=access_token, httponly=True)


        return response

    raise HTTPException(status_code=403)

@router.post("/logout")
async def user_logout(logout = Depends(delete_refresh_token)):

    return logout

@router.post("/register")
async def user_register(user: UserRegisterSchema, user_service: UserService):
    new_user = await user_service.add_new_user(user)
    return new_user


