"""
    # Database "ACADEMIC HUB"

    This file will contain the SQLAlchemy models and the database connection

    The database connection is created using SQLAlchemy. The database URL is read from the environment variables and used to create a new SQLAlchemy engine.

    The SessionLocal object is a sessionmaker that will be used to create a new session for each request. The get_db function is a dependency that will be used to get a new session for each request.
"""
from dotenv import load_dotenv

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import create_engine, Column, Integer, String

from enum import Enum
import os
import re

load_dotenv()

class UserType(Enum):
    """Enumeration for the different user types."""
    LIBRARY = "library"
    SCHOOL = "school"


def _session_factory(user_type: str) -> sessionmaker:
    """
        Creates a sessionmaker for the specified user type.

        Args: 
    """
    return sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=create_engine(
            f"postgresql://{os.getenv(f'{user_type}_USER')}:{os.getenv(f'{user_type}_PSWD')}@{os.getenv('HOST')}/{os.getenv('DB_NAME')}"
        ))

def get_db(user_type: UserType):
    """
        Yields a database session for the specified user type.

        Args:
            user_type (UserType): The user type for which to create the session.
    """
    SessionLocal = _session_factory(user_type.value)
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_school():
    SessionLocal = _session_factory(UserType.SCHOOL.value)
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_library():
    SessionLocal = _session_factory(UserType.LIBRARY.value)
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def _set_db_factory(user_type: UserType) -> Callable:
#     pass
    # todo: CHeck why this doesn't work... it should work, right?
    # get_db_school = get_db(UserType.SCHOOL)  # this works because the lambda function calls the generator function
    # get_db_library = lambda: get_db(UserType.LIBRARY)  # this works because the lambda function calls the generator function
    # get_db_general = lambda: get_db(UserType.GENERAL)  # this works because the lambda function calls the generator function


Base = declarative_base()

def base_model(schema: str = 'general_dt'):
    """
    Create base models for an specific schema.

    They all inherit from the same base class and have the same table arguments.
    """
    class CustomBaseModel:
        @declared_attr
        def __tablename__(cls):
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)).lower()

    class SchemaBaseModel(declarative_base(cls=CustomBaseModel)):
        __abstract__ = True
        __table_args__ = {'schema': schema}

    class IDBaseModel(SchemaBaseModel):
        __abstract__ = True
        id = Column(Integer, primary_key=True, index=True)

    class NamedBaseModel(IDBaseModel):
        __abstract__ = True
        name = Column(String(255), nullable=False)

    return SchemaBaseModel, IDBaseModel, NamedBaseModel
