"""
    This file will contain the SQLAlchemy models and the database connection

    The database connection is created using SQLAlchemy. The database URL is read from the environment variables and used to create a new SQLAlchemy engine.

    The SessionLocal object is a sessionmaker that will be used to create a new session for each request. The get_db function is a dependency that will be used to get a new session for each request.
"""

from fastapi import Depends, HTTPException
from fastapi import APIRouter

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import BinaryExpression, Column, Integer, String, create_engine, or_

from dotenv import load_dotenv

from typing import TypeVar, Generic, Type, List, Any, Callable
from enum import Enum
import os


# * Read the environment variables
load_dotenv()

# * Create a new SQLAlchemy engine, sessionmaker, and a Base class for the ORM models
Base = declarative_base()  # means that all the models will inherit from this class


class UserType(Enum):
    """
        Enumeration for the different user types.
    """
    LIBRARY = "library"
    SCHOOL = "school"
    # GENERAL = "general"
    # ACADEMIC = "academic"

    
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

def get_db_school():
    """
        Yields a database session for the school user type.

        Args:
    """
    SessionLocal = _session_factory(UserType.SCHOOL.value)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_library():
    """
        Yields a database session for the library user type.

        Args:
    """
    SessionLocal = _session_factory(UserType.LIBRARY.value)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




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


def dt_route(model: Type[Base], router: APIRouter, db_dependency: Callable, crud_model: CRUDBase):
    @router.get(f"/{model.__tablename__}/dt/", tags=[model.__tablename__.capitalize()])
    def get_columns():
        return crud_model.get_columns()

    @router.get(f"/{model.__tablename__}/", tags=[model.__tablename__.capitalize()])
    def get_all(db: Session = Depends(db_dependency)):
        return crud_model.get_all(db)

def some_attr_route(attribute: str, model: Type[Base], router: APIRouter, db_dependency: Callable, crud_util: CRUDBase):
    """
    Creates a route to get records by a specific attribute.
    
    Args:
        attribute (str): The name of the attribute for filtering.
        model (Type[Base]): The SQLAlchemy model class.
        router (APIRouter): The FastAPI router to which the endpoint will be added.
        db_dependency (Callable): Dependency that provides a DB session.
        crud_util (CRUDBase[T]): The CRUD utility instance for the model.
    """
    @router.get(f"/{model.__tablename__}/{attribute}={{value}}", tags=[model.__tablename__.capitalize()])
    def get_by_attribute(value: str, db: Session = Depends(db_dependency)):
        return crud_util.get_by_attribute(db, attribute, value)



def all_attr_route(model: Type[Base], router: APIRouter, db_dependency: Callable):
    for column in model.__table__.columns.keys():
        some_attr_route(column, model, router, db_dependency, CRUDBase(model))


# Create a customizable base class generator function
def base_model(schema='default_schema'):
    Base = declarative_base()

    class ID_BaseModel(Base):
        __abstract__ = True  # Make this class abstract so it is not created as a table
        __table_args__ = {'schema': schema}

        id = Column(Integer, primary_key=True, index=True)

    class Named_BaseModel(ID_BaseModel):
        __abstract__ = True

        name = Column(String(255), nullable=False)

    return ID_BaseModel, Named_BaseModel


# todo: define a "get_resource_generic" function that will be used to get a resource from the database based on a model and a condition
# def crud_routes(model: Type[Base], router: APIRouter, db_dependency: Callable):
#     crud_util = CRUDBase(model)



# * GET method (Read)
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


# def // get_operations(model, any):
#     """
#     Wrapper function to create endpoints for fetching column names and all records of a model.
#     Uses the class name in lowercase for the endpoint paths.
#     """
    
#     @any.get(f"/{model.__name__.lower()}s/dt/", tags=[model.__name__])
#     def get_model_column_names():
#         """
#         Endpoint to fetch column names of the model.
#         """
#         return [c.name for c in model.__table__.columns]

# # PUT NAME USING ONLY THE FIRST LETTER AS UPPERCASE
#     @any.get(f"/{model.__name__.lower()}s/", tags=[model.__name__])    
#     def get_all_model_records(db: Session = Depends(get_db)):
#         """
#         Endpoint to fetch all records of the model.
#         """
#         return get_resource_generic(db, model)

#     @any.get(f"/{model.__name__.lower()}/id={id}", tags=[model.__name__])
#     def get_user_by_id(id: int, db: Session = Depends(get_db)):
#         return get_resource_generic(db, model, model.id == id)
    

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
