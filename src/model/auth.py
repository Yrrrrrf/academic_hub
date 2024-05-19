from functools import partial
import time
from typing import Optional
from pydantic import *
from sqlalchemy import JSON, Column, String, DateTime
import datetime

from src.database import *




SchemaBaseModel, IDBaseModel, NamedBaseModel = base_model(schema='auth')


class GeneralUser(NamedBaseModel):
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    additional_info = Column(JSON, nullable=True)


# * Pydantic Models
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password_hash: str  # for password hashing
    additional_info: Optional[dict] = {}


# This is the model that will be returned to the user when 
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    additional_info: Optional[dict] = {}  # this is the additional info field

    class Config:
        # orm_mode = True
        from_attributes = True  # same as orm_mode bug has been renamed...

auth_classes: list = get_classes_from_globals(globals())
# remove UserCreate from the list
auth_classes.remove(UserCreate)


# ? AUTH STUFF --------------------------------------------------------------------------------------


import jwt
from datetime import datetime, timedelta

import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))



SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")




class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str



from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from fastapi import Security



# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
api_key_scheme = APIKeyHeader(name="Authorization")


# Dependency to get the current user from the token
def get_current_user(token: str = Depends(api_key_scheme), db: Session = Depends(partial(get_db, "school"))):
    if token.startswith("Bearer "):
        token = token[len("Bearer "):]
    payload = decode_access_token(token)
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(GeneralUser).filter(GeneralUser.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

