from auth.schemas import TokenResponse
from models import User
from fastapi.exceptions import HTTPException
from fastapi import status
from auth.utils import generate_access_token, generate_refresh_token


def _check_access(user:User) -> bool:
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='account not active')
    return True

def generate_tokens(user:User, refresh_token:str|None = None) -> TokenResponse:
    _check_access(user)
    payload = {'username':user.username, 'id':user.id, 'email':user.email}
    access_token = generate_access_token(payload)
    if not refresh_token:
        refresh_token = generate_refresh_token(payload)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)