from passlib.context import CryptContext

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_hashed_password(raw_password:str):
    return password_context.hash(raw_password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return password_context.verify(plain_password, hashed_password)