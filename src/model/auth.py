"""
    This module contains the authentication model.

    It is responsible for handling the authentication of users.

    This to make them able to access the application.
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from jwt import encode, decode


SECRET_KEY = "some secret key..."

DEFAULT_USER = {
    # "email": "test@example.com",
    "email": "string",
    "password": "string"
}


def create_token(data: dict):
    return encode(payload=data, key=SECRET_KEY, algorithm="HS256")

def decode_token(token: str) -> dict:
    return decode(jwt=token, key=SECRET_KEY, algorithms="HS256")


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        token_dt: HTTPAuthorizationCredentials = await super().__call__(request)
        dec_token = decode_token(token_dt.credentials)

        if dec_token['email'] != DEFAULT_USER['email']:
            raise HTTPException(status_code=403, detail="That email is not registered...")
        if dec_token["password"] != DEFAULT_USER["password"]:
            raise HTTPException(status_code=403, detail="Invalid password!")
