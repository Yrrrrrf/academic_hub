# 3rd party imports
from fastapi import Depends, HTTPException, APIRouter

# stdlib imports
from typing import Type, Callable

from fastapi.responses import JSONResponse

# local imports
from src.model.auth import JWTBearer
from src.model.general import *
from src.model.library import *
from src.model.school import *
from src.database import *


home: APIRouter = APIRouter()
"""
# Home Route

This route contains the main methods that will be used to display the home page of the application.

## Example
- Get the home page
- Get the about page
- Get the contact page
- Get the help page
"""
@home.get("/", tags=["home"])
def read_root(): return {"Hello From": "Home Route"}

@home.get("/penchs", tags=["home"])
def read_root(): return {"Pench's": "Hola Amix"}


# ? Test the Auth route...
# * Improve the security by adding a token to the login route to authenticate the user & authorize them to access the application.
from src.model.auth import create_token
from pydantic import BaseModel

class SomeUser(BaseModel):
    email: str
    password: str

@home.post("/token", tags=["Auth"])
# async def login(user: SomeUser):
def login(user: SomeUser):
    token: str = create_token(user.model_dump())
    return JSONResponse(content={"token": token})
    # return {"token": create_token(user.model_dump())}








# * data table routes
def _dt_routes(
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
    # @router.get(f"/{model.__tablename__.lower()}/dt/", tags=[model.__name__])  # Decorate the route function with the GET route for getting column names
    @router.get(f"/{model.__tablename__.lower()}/dt/", tags=[model.__name__])
    def get_columns(): return [c.name for c in model.__table__.columns]  # Return a list of column names

    # @router.get(f"/{model.__tablename__.lower()}s/", tags=[model.__name__], dependencies=[Depends(JWTBearer())])
    @router.get(f"/{model.__tablename__.lower()}s/", tags=[model.__name__])  # Decorate the route function with the GET route for getting all resources
    def get_all(db: Session = Depends(db_dependency)): return db.query(model).all()  # Return a list of all resources

# * crud routes
def _crud_routes(
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

    # * Create the CRUD routes for each included attribute
    included_attributes = [attr for attr in model.__table__.columns.keys() if attr not in excluded_attributes]  # Get a list of included attributes

    [_post_route(attr) for attr in included_attributes]     # * Create
    # [_get_route(attr) for attr in included_attributes]      # * Read
    [_get_route(attr) for attr in model.__table__.columns.keys()]  # * Read (with id included...)
    [_put_route(attr) for attr in included_attributes]      # * Update
    [_delete_route(attr) for attr in included_attributes]   # * Delete


# todo: Test this function
# todo: Add a way to get the view name from the model
# * views routes
def _views_routes(
    router: APIRouter, 
    db_dependency: Callable,
):
    """
    Creates views routes for a given model and router.

    Args:
        router (APIRouter): The FastAPI router to which the endpoints will be added.
        db_dependency (Callable): Dependency that provides a DB session.
    """
    @router.get("/views/{view_name}/", tags=["views"])  # Decorate the route function with the GET route for getting all resources
    def get_view(view_name: str, db: Session = Depends(db_dependency)):  # Route function to get all resources
        view = db.execute(f"SELECT * FROM {view_name}").fetchall()  # Execute a raw SQL query to get the view data
        if not view:  # If the view is empty
            raise HTTPException(
                status_code=404,
                detail=f"No view named '{view_name}' found."
            )
        return view  # Return the view data




basic_dt: APIRouter = APIRouter()  # for data table routes
crud_attr: APIRouter = APIRouter()  # crud routes for each attribute
views: APIRouter = APIRouter()  # todo: views routes... for views xd


for general_class in general_classes:
    _dt_routes(general_class, basic_dt, get_db_school)  # this is available for any db user
    _crud_routes(general_class, crud_attr, get_db_school)  # this is available for any db user

# for lib_class in lib_classes:
#     _dt_routes(lib_class, basic_dt, get_db_library)  # this is available for any db user
#     _crud_routes(lib_class, crud_attr, get_db_library)  # this is available for any db user

# for school_class in school_classes:
#     _dt_routes(school_class, basic_dt, get_db_school)  # this is available for any db user
#     _crud_routes(school_class, crud_attr, get_db_school)  # this is available for any db user


# * public routes (no authentication required)

# * views_routes(views, get_db_school)
# * views_routes(views, get_db_library)
