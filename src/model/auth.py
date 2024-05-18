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
    additional_info: Optional[dict]
    created_at: datetime.datetime

    class Config:
        orm_mode = True

auth_classes: list = get_classes_from_globals(globals())
# remove UserCreate from the list
auth_classes.remove(UserCreate)


# ? AUTH STUFF --------------------------------------------------------------------------------------


import jwt
from datetime import datetime, timedelta


# Encode a token
def create_access_token(data: dict, secret_key: str, algorithm: str, expires_delta: timedelta = None):
    to_encode = data.copy()  
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=15)})  # 15 minutes expiration
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)

# Decode a token
def decode_access_token(token: str, secret_key: str, algorithms: list):
    payload = jwt.decode(token, secret_key, algorithms=algorithms)
    return payload

# Usage
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

data = {"sub": "username"}
token = create_access_token(data, SECRET_KEY, ALGORITHM)
decoded_data = decode_access_token(token, SECRET_KEY, [ALGORITHM])
