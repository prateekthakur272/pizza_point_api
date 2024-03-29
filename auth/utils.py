from passlib.context import CryptContext
from settings import get_settings
from datetime import datetime, timedelta
from jwt import encode, decode, PyJWTError


password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
settings = get_settings()

def get_hashed_password(raw_password:str):
    return password_context.hash(raw_password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return password_context.verify(plain_password, hashed_password)

def generate_token(payload:dict, is_access:bool=False):
    data = payload.copy()
    if is_access:
        expire_in = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXP_TIME)
        data.update({'exp':expire_in})
    return encode(payload=data, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_token_data(token:str) -> dict:
    try:
        payload = decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except PyJWTError:
        return {}
    