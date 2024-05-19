from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import *

from jose import JWTError, jwt
from passlib.context import CryptContext

from functools import partial
from typing import Annotated, Optional
from datetime import datetime, timedelta
import os

from src.api.database import *
from src.model.public import GeneralUser, UserModel  # * main user model (for authentication)


# Authentication Router
auth: APIRouter = APIRouter(tags=["Auth"], prefix="/auth")

# OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login_token")

# CryptContext for hashing passwords
bcrypt_context = CryptContext(
    schemes=["bcrypt"],  # Set the hashing algorithm to bcrypt
    deprecated="auto"  # Automatically update the hash if the algorithm is deprecated
)

class Token(BaseModel):
    """Model for representing an authentication token."""
    access_token: str
    token_type: str

# Dependency for database session
db_dependency = Annotated[Session, Depends(partial(get_db, "school"))]

@auth.post("/login_token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    """
    Authenticates the user and returns a JWT token if successful.
    
    Args:
        form_data (OAuth2PasswordRequestForm): The form containing the username and password.
        db (Session): The database session.

    Returns:
        dict: The access token and token type.
    """
    user: GeneralUser = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token(user.name, user.id, timedelta(minutes=20))

    return {"access_token": token, "token_type": "bearer"}

def authenticate_user(email: str, password: str, db: Session) -> Optional[GeneralUser]:
    """
    Authenticates the user by email and password.
    
    Args:
        email (str): The user's email.
        password (str): The user's password.
        db (Session): The database session.

    Returns:
        Optional[GeneralUser]: The authenticated user or None if authentication fails.
    """
    user = db.query(GeneralUser).filter(GeneralUser.email == email).first()
    if not user:
        return None
    if not bcrypt_context.verify(password, user.password):
        return None
    return user

# Secret key and algorithm for JWT
SECRET_KEY = os.getenv("SECRET_KEY", "some_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_TIME", 30))

def create_access_token(name: str, user_id: int, expires_delta: timedelta) -> str:
    """
    Creates a JWT token.

    Args:
        name (str): The user's name.
        user_id (int): The user's ID.
        expires_delta (timedelta): The token's expiration time.

    Returns:
        str: The JWT token.
    """
    to_encode = {"sub": name, "id": user_id}
    expires = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    """
    Retrieves the current user from the JWT token.

    Args:
        token (str): The JWT token.

    Returns:
        dict: The user's information.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        return {"name": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

user_dependency = Annotated[dict, Depends(get_current_user)]

@auth.get("/users/me", response_model=UserModel)
async def user_me(user: user_dependency, db: db_dependency):
    """
    Retrieves the authenticated user's information.

    Args:
        user (dict): The current user.
        db (Session): The database session.

    Returns:
        GeneralUser: The user's information.
    """
    user = db.query(GeneralUser).filter(GeneralUser.id == user.get("id")).first()
    if user is None:
        raise HTTPException(status_code=400, detail="Authentication Required")
    return user
