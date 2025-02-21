import time
import jwt
from passlib.context import CryptContext

from src.config import Settings
from src.auth.schemas import UserLoginSchema, UserSchema, UserRegisterSchema, UserRegisterHashedSchema

JWT_SECRET = Settings.JWT_SECRET
JWT_ALGORITHM = Settings.JWT_ALGORITHM
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def sign_jwt(id: int) -> str:
    payload = {
        "user_id": id,
        "expires": time.time() + 20000
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else {}
    except:
        return {}


async def check_user(current_user: UserLoginSchema, user_from_db: UserSchema) -> bool:
    if current_user.email == user_from_db.email and await verify_password(current_user.password, user_from_db.hashed_password):
        return True
    else:
        return False


async def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

async def create_user_register_hash_schema(reg_user: UserRegisterSchema):
    return UserRegisterHashedSchema(
        name = reg_user.name,
        email = reg_user.email,
        status = reg_user.status,
        hashed_password = await hash_password(reg_user.password)
    )
