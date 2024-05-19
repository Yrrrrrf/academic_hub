from fastapi.security import APIKeyHeader, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import JSON, Column, String, DateTime
from pydantic import *

import bcrypt
from jose import JWTError, jwt
from passlib.context import CryptContext

from functools import partial
from typing import Annotated, Optional
from datetime import datetime, timedelta
import os

from src.database import *


SchemaBaseModel, IDBaseModel, NamedBaseModel = base_model(schema='auth')


class GeneralUser(NamedBaseModel):
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    additional_info = Column(JSON, nullable=True)


# * Pydantic Models
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password_hash: str  # for password hashing
    additional_info: Optional[dict] = None


# This is the model that will be returned to the user when 
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    additional_info: Optional[dict] = None

    class Config:
        # orm_mode = True  # old version of pydantic
        from_attributes = True  # same as orm_mode bug has been renamed...

auth_classes: list = get_classes_from_globals(globals())
auth_classes.remove(UserCreate)
auth_classes.remove(UserResponse)


# ? AUTH STUFF --------------------------------------------------------------------------------------


auth: APIRouter = APIRouter(tags=["Auth"], prefix="/auth")
"""
# Authentication Routes

This route contains the main methods that will be used to authenticate users.

"""


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login_token")  # path to the login route
bcrypt_context = CryptContext(
    schemes=["bcrypt"],  # sete the hashing algorithm
    deprecated="auto"  # update the hash when the algorithm is deprecated
)


class Token(BaseModel):
    access_token: str
    token_type: str

db_dependency = Annotated[Session, Depends(partial(get_db, "school"))]

@auth.post("/login_token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    user: GeneralUser = authenticate_user(form_data.username, form_data.password, db)
    if not user: raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token(user.name, user.id, timedelta(minutes=20))

    return { "access_token": token, "token_type": "bearer" }
    # return { "access_token": "asasasasas", "token_type": "bearer" }


def authenticate_user(email: str, password: str, db: Session) -> Optional[GeneralUser]:
    user = db.query(GeneralUser).filter(GeneralUser.email == email).first()
    if not user: return False
    if not bcrypt_context.verify(password, user.password_hash): return False
    return user


SECRET_KEY = os.getenv("SECRET_KEY", "some_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_TIME", 30)


def create_access_token(name: str, user_id: int, expires_delta: timedelta):
    encode = { "sub": name, "id": user_id }
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        print(username, user_id)
        print(payload)
        if user_id is None: raise HTTPException(status_code=400, detail="Invalid token")
        return { "name": username, "id": user_id }
    except JWTError: raise HTTPException(status_code=400, detail="Invalid token")

user_dependency = Annotated[dict, Depends(get_current_user)]

# * Some example of a protected route...

@auth.get("/users/me")
async def user_me(user: user_dependency, db: db_dependency):
    user = db.query(GeneralUser).filter(GeneralUser.id == user.get("id")).first()   
    match user:
        case None: raise HTTPException(status_code=400, detail="Authentication Required")
        case _: return user
