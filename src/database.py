"""
    This file will contain the SQLAlchemy models and the database connection

    The database connection is created using SQLAlchemy. The database URL is read from the environment variables and used to create a new SQLAlchemy engine.

    The SessionLocal object is a sessionmaker that will be used to create a new session for each request. The get_db function is a dependency that will be used to get a new session for each request.
"""

from dotenv import load_dotenv

from fastapi import Depends, HTTPException, APIRouter

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import BinaryExpression, Column, Integer, String, create_engine

from typing import TypeVar, Generic, Type, Callable, List, Any
from enum import Enum
import os
import re


# * Read the environment variables
load_dotenv()


class UserType(Enum):
    """
        Enumeration for the different user types.
    """
    LIBRARY = "library"
    SCHOOL = "school"
    # GENERAL = "general"
    # OWNER = "some"

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

def get_db_general():
    SessionLocal = _session_factory(UserType.GENERAL.value)
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




# todo: Check if base_model & CRUDBase can be a single class

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


Base = declarative_base()

T = TypeVar('T', bound=Base)

class CRUDBase(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def get_columns(self) -> List[str]:
        return [c.name for c in self.model.__table__.columns]

    def get_all(self, db: Session) -> List[T]:
        return get_resource_generic(db, self.model)

    def get_by_attribute(self, db: Session, attribute: str, value: Any) -> List[T]:
        """
        Fetches records by a given attribute and its value.
        
        Args:
            db (Session): The database session.
            attribute (str): The attribute name to filter by.
            value (Any): The value of the attribute to match.
            
        Returns:
            A list of model instances that match the attribute value.
        """
        # Dynamically get the attribute from the model
        model_attribute = getattr(self.model, attribute, None)
        if not model_attribute:
            raise HTTPException(status_code=400, detail=f"Attribute {attribute} not found in model {self.model.__name__}.")
        return db.query(self.model).filter(model_attribute == value).all()


def dt_route(model: Type[Base], router: APIRouter, db_dependency: Callable):
    @router.get(f"/{model.__tablename__.lower()}/dt/", tags=[model.__name__])
    def get_columns():
        return CRUDBase(model).get_columns()

    @router.get(f"/{model.__tablename__.lower()}s/", tags=[model.__name__])
    def get_all(db: Session = Depends(db_dependency)):
        return CRUDBase(model).get_all(db)
        

def get_attr_route(attribute: str, model: Type[Base], router: APIRouter, db_dependency: Callable):
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
        # return CRUDBase(model).get_by_attribute(db, attribute, value)
        return CRUDBase(model).get_by_attribute(db, attribute, value)

def get_all_attr_route(model: Type[Base], router: APIRouter, db_dependency: Callable):
    [get_attr_route(column, model, router, db_dependency) for column in model.__table__.columns.keys()]










def get_resource_generic(db: Session, model: Type[Base], condition: BinaryExpression = True) -> Any: # type: ignore
    """
    This method will be used to get a resource from the database based on a model and a condition.

    Args:
        - db (Session): The database session
        - model (Type[Base]): The model to use
    - condition (BinaryExpression): The condition to use to filter the resources
            - if no condition is provided, all the resources will be returned
    """
    # resource = db.query(model).filter(condition).all()
    # if not resource:
    #     raise HTTPException(status_code=404, detail=f"{model.__tablename__.capitalize()} not found")
    # return resource
    # ^ Just check this code... it's the same as the one below but without the if statement :3
    return db.query(model).filter(condition).all() or \
        (_ for _ in ()).throw(HTTPException(status_code=404, detail=f"{model.__name__.capitalize()} not found"))
        # (_ for _ in ()).throw(HTTPException(status_code=404, detail=f"{model.__tablename__.capitalize()} not found"))


# ? TEST --------------------------------------------------------------------------------------


# todo: Test this method
# * POST method (Create)
def create_resource_generic(db: Session, model: Type[Base], data: dict) -> Any:  # type: ignore
    """
    This method will be used to create a new resource in the database based on a model and some data.

    Args:
        - db (Session): The database session
        - model (Type[Base]): The model to use
        - data (dict): The data to use to create the new resource
    """
    new_resource = model(**data)
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource
