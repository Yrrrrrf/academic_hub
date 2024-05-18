"""
    # Database "ACADEMIC HUB"

    This file will contain the SQLAlchemy models and the database connection

    The database connection is created using SQLAlchemy. The database URL is read from the environment variables and used to create a new SQLAlchemy engine.

    The SessionLocal object is a sessionmaker that will be used to create a new session for each request. The get_db function is a dependency that will be used to get a new session for each request.
"""
# ? 3rd party imports
from dotenv import load_dotenv

from fastapi import Depends, HTTPException, APIRouter

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base, declared_attr

# ? Local imports
import os
import re
from typing import Type, Callable


# os.environ.clear()  # * Clear all environment variables (to avoid conflicts with old values)
load_dotenv()  # * Load environment variables from .env file


PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PUBLIC_KEY = os.getenv("PUBLIC_KEY")


def get_db(user_type: str):
    """
        Yields a database session for the specified user type.

        Args:
            user_type (str): The user type for the database connection.
    """
    db_url = f"postgresql://{os.getenv(f'{user_type}_ADMIN')}:{os.getenv(f'{user_type}_PWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    # db_url = f"postgresql://postgres:fire@localhost/academic_hub"
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



# * data table routes
def dt_routes(
    model: Type[Base],  # type: ignore
    router: APIRouter, 
    db_dependency: Callable, 
):
    """
    Creates CRUD routes for a given model and router.

    Args:
        model (Type[Base]): The SQLAlchemy model class.
        router (APIRouter): The FastAPI router to which the endpoints will be added.
        db_dependency (Callable): Dependency that provides a DB session.
        excluded_attributes (list[str]): List of attributes to exclude from CRUD operations.
    """
    @router.get(f"/{model.__tablename__.lower()}/dt", tags=[model.__name__])
    def get_columns(): return [c.name for c in model.__table__.columns]  # Return a list of column names

    @router.get(f"/{model.__tablename__.lower()}s", tags=[model.__name__])  # Decorate the route function with the GET route for getting all resources
    def get_all(db: Session = Depends(db_dependency)): return db.query(model).all()  # Return a list of all resources

# * crud routes
# todo: Modify this methods to return a JSON response (to be more RESTful)
def crud_routes(
    model: Type[Base],  # type: ignore ---- The SQLAlchemy model class
    router: APIRouter,  # The FastAPI router to which the endpoints will be added
    db_dependency: Callable,  # Dependency that provides a DB session
    excluded_attributes: list[str] = ["id"],  # List of attributes to exclude from CRUD operations (default: ["id"])
):
    """
    Creates CRUD routes for a given model and router.

    Args:
        model (Type[Base]): The SQLAlchemy model class.
        router (APIRouter): The FastAPI router to which the endpoints will be added.
        db_dependency (Callable): Dependency that provides a DB session.
        excluded_attributes (list[str]): List of attributes to exclude from CRUD operations.
    """

    def _post_route(attribute: str):  # Function to create a POST route for a given attribute
        @router.post(f"/{model.__tablename__.lower()}/{attribute}={{value}}", tags=[model.__name__])  # Decorate the route function with the POST route
        def create_by_attribute(value: str, data: dict, db: Session = Depends(db_dependency)):  # Route function to create a new resource
            data[attribute] = value  # Add the attribute value to the data dictionary
            new_resource = model(**data)  # Create a new instance of the model with the provided data
            db.add(new_resource)  # Add the new resource to the database session
            db.commit()  # Commit the transaction (save the new resource to the database)
            db.refresh(new_resource)  # Refresh the new resource (e.g., to get the assigned ID)
            return new_resource  # Return the new resource as a response

    def _get_route(attribute: str):  # Function to create a GET route for a given attribute
        @router.get(f"/{model.__tablename__.lower()}/{attribute}={{value}}", tags=[model.__name__])  # Decorate the route function with the GET route
        def get_by_attribute(value: str, db: Session = Depends(db_dependency)):  # Route function to get resources
            result = db.query(model).filter(getattr(model, attribute) == value).all()  # Get resources matching the attribute value
            if not result:  # If no resources were found
                raise HTTPException(
                    status_code=404,
                    detail=f"No {model.__tablename__.capitalize()} with the form '{attribute} == {value}' found."
                )
            return result  # Return the list of resources

    def _put_route(attribute: str):  # Function to create a PUT route for a given attribute
        @router.put(f"/{model.__tablename__.lower()}/{attribute}={{value}}", tags=[model.__name__])  # Decorate the route function with the PUT route
        def update_by_attribute(value: str, data: dict, db: Session = Depends(db_dependency)):  # Route function to update resources
            condition = getattr(model, attribute) == value  # Create a condition to filter resources by the attribute value
            result = db.query(model).filter(condition).update(data, synchronize_session=False)  # Update resources matching the condition
            db.commit()  # Commit the transaction (save the updates)
            if result == 0:  # If no resources were updated
                raise HTTPException(
                    status_code=404,
                    detail=f"No {model.__tablename__.capitalize()} found with {attribute}={value}."
                )
            return {
                "message": f"Successfully updated {result} record(s) in {model.__tablename__.capitalize()}.",
                "updated_count": result,
            }

    def _delete_route(attribute: str):  # Function to create a DELETE route for a given attribute
        @router.delete(f"/{model.__tablename__.lower()}/{attribute}={{value}}", tags=[model.__name__])  # Decorate the route function with the DELETE route
        def delete_by_attribute(value: str, db: Session = Depends(db_dependency)):  # Route function to delete resources
            condition = getattr(model, attribute) == value  # Create a condition to filter resources by the attribute value
            result = db.query(model).filter(condition).delete(synchronize_session=False)  # Delete resources matching the condition
            if result == 0:  # If no resources were deleted
                raise HTTPException(
                    status_code=404,
                    detail=f"No {model.__name__} with the form '{condition.left.description} == {condition.right.value}' found."
                )
            db.commit()  # Commit the transaction (save the deletions)
            return {
                "message": f"Successfully deleted {result} record(s) from {model.__tablename__.capitalize()}.",
                "deleted_count": result,
            }

    def _post_new_route():
        @router.post(f"/{model.__tablename__.lower()}", tags=[model.__name__])  # Decorate the route function with the POST route
        def create_new(data: dict, db: Session = Depends(db_dependency)):  # Route function to create a new resource
            new_resource = model(**data)  # Create a new instance of the model with the provided data
            db.add(new_resource)  # Add the new resource to the database session
            db.commit()  # Commit the transaction (save the new resource to the database)
            db.refresh(new_resource)  # Refresh the new resource (e.g., to get the assigned ID)
            return new_resource  # Return the new resource as a response


    # * Create the CRUD routes for each included attribute
    included_attributes = [attr for attr in model.__table__.columns.keys() if attr not in excluded_attributes]  # Get a list of included attributes

    # [_post_route(attr) for attr in included_attributes]     # Create (by attribute)
    # [_get_route(attr) for attr in included_attributes]      # Read (by attribute)
    _post_new_route()  # * Create (new resource with all attributes included)
    [_get_route(attr) for attr in model.__table__.columns.keys()]  # * Read (with id comlumn included...)
    [_put_route(attr) for attr in included_attributes]      # * Update
    [_delete_route(attr) for attr in included_attributes]   # * Delete


