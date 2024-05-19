from sqlalchemy import JSON, Column, String, DateTime
from pydantic import *

from typing import Optional
from datetime import datetime

from src.api.database import *


# * SQL ALchemy Model 
class GeneralUser(Base):
    __tablename__ = "general_user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    additional_info = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<User {self.name}>"


# * Pydantic Models
class UserModel(BaseModel):
    name: str
    email: EmailStr
    password: str  # for password hashing
    additional_info: Optional[dict] = None

    class Config:
        # orm_mode = True  # old version of pydantic
        from_attributes = True  # same as orm_mode bug has been renamed...

auth_classes: list = get_classes_from_globals(globals())
auth_classes.remove(UserModel)
