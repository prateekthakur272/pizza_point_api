from fastapi.security import OAuth2PasswordBearer
from auth.schemas import TokenResponse
from models import User
from fastapi.exceptions import HTTPException
from fastapi import Depends, status
from sqlalchemy.orm import Session
from database import get_db_session
from auth.utils import generate_token, get_token_data
from mailer.mailer import send_verification_mail


oauth_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

async def _check_access(user:User) -> bool:
    if not user.is_active:
        await send_verification_mail(user)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='account not active, click on the link sent by email')
    return True

async def generate_tokens(user:User, refresh_token:str|None = None) -> TokenResponse:
    await _check_access(user)
    payload = {'username':user.username, 'id':user.id, 'email':user.email}
    access_token = generate_token(payload, is_access=True)
    if not refresh_token:
        refresh_token = generate_token(payload)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

def refresh_access_token(refresh_token:str) -> TokenResponse:
    payload = get_token_data(refresh_token)
    user_id = payload.get('id', None)
    db = next(get_db_session())
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid refresh token')
    return generate_tokens(user, refresh_token=refresh_token)

def validate_token(token:str, db:Session)->User:
    payload = get_token_data(token)
    user = db.query(User).filter(User.id == payload.get('id', None)).first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid token')

def get_current_user(token:str = Depends(oauth_scheme), db:Session = Depends(get_db_session)):
    return validate_token(token, db)