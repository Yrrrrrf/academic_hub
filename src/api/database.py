"""
    # Database "ACADEMIC HUB"

    This file will contain the SQLAlchemy models and the database connection

    The database connection is created using SQLAlchemy. The database URL is read from the environment variables and used to create a new SQLAlchemy engine.

    The SessionLocal object is a sessionmaker that will be used to create a new session for each request. The get_db function is a dependency that will be used to get a new session for each request.
"""
from dotenv import load_dotenv

from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base, declared_attr

import re
from typing import Dict, Optional, Type, Any, List

# os.environ.clear()  # * Clear all environment variables (to avoid conflicts with old values)
load_dotenv()  # * Load environment variables from .env file


def get_db(user_type: str):
    """
        Yields a database session for the specified user type.

        Args:
            user_type (str): The user type for the database connection.
    """
    # db_url = f"postgresql://{os.getenv(f'{user_type}_ADMIN')}:{os.getenv(f'{user_type}_PWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    db_url = f"postgresql://postgres:fire@localhost/academic_hub"
    print(f"Connecting to {user_type} database at {db_url}")
    db: Session = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(db_url))()
    try:
        yield db
    finally:
        db.close()

def get_classes_from_globals(globals_dict) -> list:
    """
    Retrieve a list of classes defined in the given global scope.
    
    :param globals_dict: The globals() dictionary from the calling module.
    :return: A list of class objects defined in the global scope.
    """
    return [obj for name, obj in globals_dict.items() if isinstance(obj, type) and obj.__module__ == globals_dict['__name__']]

Base = declarative_base()

#  * Helper function to create base models (abstract classes) for SQLAlchemy models
def base_model(schema: str = 'public'):
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

# * Helper function to create Pydantic models from SQLAlchemy models
def create_pydantic_model(
    sqlalchemy_model: Type[Base],  # type: ignore 
    pydantic_base_model: Type[BaseModel]
) -> Type[BaseModel]:
    annotations: Dict[str, Any] = {}
    for column in sqlalchemy_model.__table__.columns:
        python_type = column.type.python_type if hasattr(column.type, 'python_type') else str
        annotations[column.name] = Optional[python_type] if column.nullable else python_type

    # Create a dictionary of attributes to be used in the Pydantic model
    pydantic_attributes: Dict[str, Any] = {'__annotations__': annotations}

    return type(f"{sqlalchemy_model.__name__}Pydantic", (pydantic_base_model,), pydantic_attributes)

