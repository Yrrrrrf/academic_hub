"""
    # Database "ACADEMIC HUB"

    This file will contain the SQLAlchemy models and the database connection

    The database connection is created using SQLAlchemy. The database URL is read from the environment variables and used to create a new SQLAlchemy engine.

    The SessionLocal object is a sessionmaker that will be used to create a new session for each request. The get_db function is a dependency that will be used to get a new session for each request.
"""
from dotenv import load_dotenv

from fastapi import Depends, HTTPException, APIRouter

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import create_engine, BinaryExpression, Column, Integer, String

from typing import Type, Callable, Any
from enum import Enum
import os
import re

# from contextlib import contextmanager

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

# @contextmanager
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
#     # todo: CHeck why this doesn't work... it should work, right?
#     # get_db_school = get_db(UserType.SCHOOL)  # this works because the lambda function calls the generator function
#     # get_db_library = lambda: get_db(UserType.LIBRARY)  # this works because the lambda function calls the generator function
#     # get_db_general = lambda: get_db(UserType.GENERAL)  # this works because the lambda function calls the generator function


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


# ^ Testings
# * POST method (Create)
def create_attr_route(attribute: str, model: Type[Base], router: APIRouter, db_dependency: Callable): # type: ignore
    """
    Creates a route to create a record with a specific attribute.

    Args:
        attribute (str): The name of the attribute for filtering.
        model (Type[Base]): The SQLAlchemy model class.
        router (APIRouter): The FastAPI router to which the endpoint will be added.
        db_dependency (Callable): Dependency that provides a DB session.
    """
    @router.post(f"/{model.__tablename__.lower()}/{attribute}={{value}}", tags=[model.__name__])
    def create_by_attribute(value: str, data: dict, db: Session = Depends(db_dependency)):
        data[attribute] = value  # Add the attribute to the data
        # return create_resource_generic(db, model, data)

        # same as above but inlined
        new_resource = model(**data)  # Create a new resource (class instance)
        db.add(new_resource)  # Add the new resource to the database session
        db.commit()  # * Commit the transaction (save the new resource to the database)
        db.refresh(new_resource)  # Update the `id` attribute of the new resource (from the database)
        return new_resource  # Return the new resource as a response

def create_all_attr_route(model: Type[Base], router: APIRouter, db_dependency: Callable): # type: ignore
    # [create_attr_route(column, model, router, db_dependency) for column in model.__table__.columns.keys()]
    columns: list[str] = model.__table__.columns.keys()
    # todo: remove the id column from the list of columns (for the POST method)
    columns.remove('id')
    [create_attr_route(column, model, router, db_dependency) for column in columns]


# * PUT method (Update)
def update_attr_route(attribute: str, model: Type[Base], router: APIRouter, db_dependency: Callable):  # type: ignore
    """
    Creates a route to update records by a specific attribute.

    Args:
        attribute (str): The name of the attribute for filtering.
        model (Type[Base]): The SQLAlchemy model class.
        router (APIRouter): The FastAPI router to which the endpoint will be added.
        db_dependency (Callable): Dependency that provides a DB session.
    """
    @router.put(f"/{model.__tablename__.lower()}/{attribute}={{value}}", tags=[model.__name__])
    def update_by_attribute(value: str, data: dict, db: Session = Depends(db_dependency)):
        condition: BinaryExpression = getattr(model, attribute) == value
        result = db.query(model).filter(condition)
        result.update(data, synchronize_session=False)
        db.commit()
        if result == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No {model.__tablename__.capitalize()} found with {attribute}={value}."
            )
        return {
            "message": f"Successfully updated {result} record(s) in {model.__tablename__.capitalize()}.",
            "updated_count": result,
        }

def update_all_attr_route(model: Type[Base], router: APIRouter, db_dependency: Callable):  # type: ignore
    """
    Automatically generates update routes for all attributes of the model.

    Args:
        model (Type[Base]): The SQLAlchemy model class.
        router (APIRouter): The FastAPI router.
        db_dependency (Callable): Dependency that provides a DB session.
    """
    columns: list[str] = model.__table__.columns.keys()
    columns.remove('id')
    [update_attr_route(column, model, router, db_dependency) for column in columns]



# * CORRECT!
# * GET method (Read)

def dt_route(model: Type[Base], router: APIRouter, db_dependency: Callable): # type: ignore
    @router.get(f"/{model.__tablename__.lower()}/dt/", tags=[model.__name__])
    def get_columns():
        return [c.name for c in model.__table__.columns]

    @router.get(f"/{model.__tablename__.lower()}s/", tags=[model.__name__])
    def get_all(db: Session = Depends(db_dependency)):
        return db.query(model).all()

def get_attr_route(attribute: str, model: Type[Base], router: APIRouter, db_dependency: Callable): # type: ignore
    """
    Creates a route to get records by a specific attribute.
    
    Args:
        attribute (str): The name of the attribute for filtering.
        model (Type[Base]): The SQLAlchemy model class.
        router (APIRouter): The FastAPI router to which the endpoint will be added.
        db_dependency (Callable): Dependency that provides a DB session.
    """
    @router.get(f"/{model.__tablename__.lower()}/{attribute}={{value}}", tags=[model.__name__])
    def get_by_attribute(value: str, db: Session = Depends(db_dependency)):
        result: Any = db.query(model).filter(getattr(model, attribute) == value).all()
        match result:
            case []:
                raise HTTPException(
                    status_code=404,
                    detail=f"No {model.__tablename__.capitalize()} with the form '{attribute} == {value}' found."
                )
            case _:
                return result

def get_all_attr_route(model: Type[Base], router: APIRouter, db_dependency: Callable): # type: ignore
    [get_attr_route(column, model, router, db_dependency) for column in model.__table__.columns.keys()]

# * DELETE method (Delete)

def delete_attr_route(attribute: str, model: Type[Base], router: APIRouter, db_dependency: Callable): # type: ignore
    """
    Creates a route to delete records by a specific attribute.
    
    Args:
        attribute (str): The name of the attribute for filtering.
        model (Type[Base]): The SQLAlchemy model class.
        router (APIRouter): The FastAPI router to which the endpoint will be added.
        db_dependency (Callable): Dependency that provides a DB session.
    """
    @router.delete(f"/{model.__tablename__.lower()}/{attribute}={{value}}", tags=[model.__name__])
    def delete_by_attribute(value: str, db: Session = Depends(db_dependency)):
        condition: BinaryExpression = getattr(model, attribute) == value
        result = db.query(model).filter(condition).delete(synchronize_session=False)
        match result:
            case 0:
                raise HTTPException(
                    status_code=404,
                    detail=f"No {model.__name__} with the form '{condition.left.description} == {condition.right.value}' found."
                )
            case _:
                db.commit()
                return {
                    "message": f"Successfully deleted {result} record(s) from {model.__tablename__.capitalize()}.",
                    "deleted_count": result
                }
    
def delete_all_attr_route(model: Type[Base], router: APIRouter, db_dependency: Callable): # type: ignore
    [delete_attr_route(column, model, router, db_dependency) for column in model.__table__.columns.keys()]
