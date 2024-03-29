from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi import Depends, Header, status
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db_session
from sqlalchemy.orm import Session
from auth.schemas import TokenResponse, UserResponse, UserSignUp
from models import User
from auth.utils import get_hashed_password, verify_password
from auth.services import generate_tokens, get_current_user, refresh_access_token, validate_token
from mailer.mailer import send_verification_mail

auth_router = APIRouter(prefix='/auth', tags=['Authentication'])

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def sign_up(user:UserSignUp, db:Session = Depends(get_db_session)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='A user with same email already exists')
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='A user with same username already exists')
    new_user = User(**user.model_dump(exclude='password'), password=get_hashed_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    await send_verification_mail(new_user)
    return JSONResponse({'message':f'user created with email:{user.email}, click on verification link in email to verify account'})

@auth_router.post('/login', response_class=JSONResponse, response_model=TokenResponse, response_model_exclude_none=True, status_code=status.HTTP_200_OK)
async def login(data:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db_session)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        user = db.query(User).filter(User.email == data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid password')
    return await generate_tokens(user)

@auth_router.get('/me', response_model=UserResponse, response_class=JSONResponse, response_model_exclude_none=True)
async def get_user(user:User = Depends(get_current_user)):
    return user

@auth_router.get('/refresh', response_class=JSONResponse, response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(Refresh_Token:str = Header()):
    return refresh_access_token(Refresh_Token)

@auth_router.get('/verification', response_class=JSONResponse, status_code=status.HTTP_200_OK)
def verify_email(token:str, db:Session = Depends(get_db_session)):
    user = validate_token(token, db)
    user.is_active = True
    db.commit()
    return {'message':'account verified!, you can now login to your account'}