"""
    # Database "ACADEMIC HUB"

    This file will contain the SQLAlchemy models and the database connection

    The database connection is created using SQLAlchemy. The database URL is read from the environment variables and used to create a new SQLAlchemy engine.

    The SessionLocal object is a sessionmaker that will be used to create a new session for each request. The get_db function is a dependency that will be used to get a new session for each request.
"""
# ? 3rd party imports
from dotenv import load_dotenv

from fastapi import Depends, HTTPException, APIRouter

from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base, declared_attr

# ? Local imports
import os
import re
from typing import Dict, List, Optional, Type, Callable, Any

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
    sqlalchemy_model: Type[Base], 
    pydantic_base_model: Type[BaseModel]
) -> Type[BaseModel]:
    annotations: Dict[str, Any] = {}
    for column in sqlalchemy_model.__table__.columns:
        python_type = column.type.python_type if hasattr(column.type, 'python_type') else str
        annotations[column.name] = Optional[python_type] if column.nullable else python_type

    # Create a dictionary of attributes to be used in the Pydantic model
    pydantic_attributes: Dict[str, Any] = {'__annotations__': annotations}

    return type(f"{sqlalchemy_model.__name__}Pydantic", (pydantic_base_model,), pydantic_attributes)


# * DYNAMIC ROUTE GENERATORS -----------------------------------------------------------------------------------------------


# * Data Table Routes (get columns & get all data)

def dt_routes(
    sqlalchemy_model: Type[Base],  # type: ignore
    pydantic_model: Type[BaseModel],
    router: APIRouter,
    db_dependency: Callable
):
    @router.get(f"/{sqlalchemy_model.__tablename__.lower()}/dt", tags=[sqlalchemy_model.__name__], response_model=List[str])
    def get_columns(): return [c.name for c in sqlalchemy_model.__table__.columns]

    @router.get(f"/{sqlalchemy_model.__tablename__.lower()}s", tags=[sqlalchemy_model.__name__], response_model=List[pydantic_model])
    def get_all(db: Session = Depends(db_dependency)): return db.query(sqlalchemy_model).all()

# * CRUD Operations Routes (GET, POST, PUT, DELETE)

def crud_routes(
    sqlalchemy_model: Type[Base],  # type: ignore
    pydantic_model: Type[BaseModel],
    router: APIRouter,
    db_dependency: Callable,
    excluded_attributes: List[str] = [
        "id", 
        "created_at", 
        "password_hash", 
        "additional_info"
    ]
):
    """
    Creates CRUD routes for a given model.

    Args:
        model (Type[Base]): The SQLAlchemy model class.
        create_model (Type[BaseModel]): The Pydantic model class for request validation (POST).
        update_model (Type[BaseModel]): The Pydantic model class for request validation (PUT).
        response_model (Type[BaseModel]): The Pydantic model class for response formatting.
        router (APIRouter): The FastAPI router to which the endpoints will be added.
        db_dependency (Callable): Dependency that provides a DB session.
        excluded_attributes (List[str]): List of attributes to exclude from CRUD operations (default: ["id"]).
    """
    # # # * POST (Create)
    @router.post(f"/{sqlalchemy_model.__tablename__.lower()}", tags=[sqlalchemy_model.__name__], response_model=pydantic_model)
    def create_resource(resource: pydantic_model, db: Session = Depends(db_dependency)):
        # db_resource: Base = sqlalchemy_model(**resource.dict())  # Create a new resource instance
        db_resource: Base = sqlalchemy_model(**resource.model_dump())  # Create a new resource instance  # type: ignore
        db.add(db_resource)
        try:
            db.commit()
            db.refresh(db_resource)
        except Exception as e:
            db.rollback()  # Rollback the transaction
            raise e  # Raise the exception
        return db_resource  # Return the resource data

    # * GET (Read)
    def _get_route(attribute: str, attribute_type: Any):
        if attribute_type == Integer:
            param_type = int
        elif attribute_type == String:
            param_type = str
        else:
            param_type = str  # Default to str if type is unknown

        @router.get(f"/{sqlalchemy_model.__tablename__.lower()}/{attribute}={{value}}", tags=[sqlalchemy_model.__name__], response_model=List[pydantic_model])
        def get_resource(value: param_type, db: Session = Depends(db_dependency)):  # type: ignore
            result = db.query(sqlalchemy_model).filter(getattr(sqlalchemy_model, attribute) == value).all()
            if not result:
                raise HTTPException(status_code=404, detail=f"No {sqlalchemy_model.__name__} with {attribute} '{value}' found.")
            return result

    # * PUT (Update)
    def _put_route(attribute: str, attribute_type: Any):
        if attribute_type == Integer:
            param_type = int
        elif attribute_type == String:
            param_type = str
        else:
            param_type = str  # Default to str if type is unknown

        @router.put(f"/{sqlalchemy_model.__tablename__.lower()}/{attribute}={{value}}", tags=[sqlalchemy_model.__name__], response_model=pydantic_model)
        def update_resource(value: param_type, resource: pydantic_model, db: Session = Depends(db_dependency)):  # type: ignore
            condition = getattr(sqlalchemy_model, attribute) == value
            db_resource = db.query(sqlalchemy_model).filter(condition).first()
            if not db_resource:
                raise HTTPException(status_code=404, detail=f"No {sqlalchemy_model.__name__} with {attribute} '{value}' found.")

            for key, value in resource.dict(exclude_unset=True).items():
                setattr(db_resource, key, value)

            try:
                db.commit()
                db.refresh(db_resource)
            except Exception as e:
                db.rollback()
                raise e

            return db_resource

    # * DELETE (Delete)
    def _delete_route(attribute: str, attribute_type: Any):
        if attribute_type == Integer:
            param_type = int
        elif attribute_type == String:
            param_type = str
        else:
            param_type = str  # Default to str if type is unknown

        @router.delete(f"/{sqlalchemy_model.__tablename__.lower()}/{attribute}={{value}}", tags=[sqlalchemy_model.__name__])
        def delete_resource(value: param_type, db: Session = Depends(db_dependency)):  # type: ignore
            condition = getattr(sqlalchemy_model, attribute) == value
            db_resource = db.query(sqlalchemy_model).filter(condition).first()
            if not db_resource:
                raise HTTPException(status_code=404, detail=f"No {sqlalchemy_model.__name__} with {attribute} '{value}' found.")

            try:
                db.delete(db_resource)
                db.commit()
            except Exception as e:
                db.rollback()
                raise e

            return {
                "message": f"Successfully deleted {sqlalchemy_model.__name__} with {attribute} '{value}'",
                "resource": db_resource
                }

    included_attributes = [
        (attr, col.type.__class__)
        for attr, col in sqlalchemy_model.__table__.columns.items()
        if attr not in excluded_attributes
    ]

    for attr, attr_type in included_attributes:
        _get_route(attr, attr_type)
        _put_route(attr, attr_type)
        _delete_route(attr, attr_type)
