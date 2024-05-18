from sqlalchemy import JSON, Column, String, DateTime
import datetime

from src.database import *


SchemaBaseModel, IDBaseModel, NamedBaseModel = base_model(schema='auth')


class GeneralUser(NamedBaseModel):
    email = Column(String(255), index=True, nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    additional_info = Column(JSON, default={})


auth_classes: list = get_classes_from_globals(globals())


# ? AUTH STUFF --------------------------------------------------------------------------------------


from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
# * JSON Web Token (JWT)
from jwt import encode, decode


ALGORITHM: str = "HS256"

DEFAULT_USER: dict = {
  "email": "admin@localhost",
  "password": "some_admin_password",
}


def create_token(data: dict):
    return encode(payload=data, key=PRIVATE_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    return decode(jwt=token, key=PRIVATE_KEY, algorithms=[ALGORITHM])


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        token_dt: HTTPAuthorizationCredentials = await super().__call__(request)
        dec_token = decode_token(token_dt.credentials)

        if dec_token['email'] != DEFAULT_USER['email']:
            raise HTTPException(status_code=403, detail="That email is not registered...")
        if dec_token["password"] != DEFAULT_USER["password"]:
            raise HTTPException(status_code=403, detail="Invalid password!")
