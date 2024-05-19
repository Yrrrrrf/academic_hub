# 3rd party imports
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import Integer, String
from sqlalchemy.orm import Session
from pydantic import BaseModel
import bcrypt

# stdlib imports
from typing import List, Type, Callable, Any
from functools import partial


# local imports
from src.database import *
from src.model.auth import *
from src.model.infrastructure import *
from src.model.library import *
from src.model.school import *


def define_routes():
    home: APIRouter = APIRouter()  # for home routes
    """
    # Home Route

    This route contains the main methods that will be used to display the home page of the application.

    ## Example
    - Get the home page
    - Get the about page
    - Get the contact page
    - Get the help page
    """

    # @home.get("/", tags=["Main"])  # todo: Make this rout a redirect to the main web interface (svelte app) on the future...
    # def _home_route(): return {"The interface for Academic Hub API is on: 127.0.0.1:8000/docs"}

    basic_dt: APIRouter = APIRouter()  # for data table routes
    """
    # Data Table Routes

    This routes contains some basic useful methods for the data tables.

    ## Example
    - Get the attributes of a table (all the columns)
    - Get all the resources of a table (all the rows)
    """

    crud_attr: APIRouter = APIRouter()  # crud routes for each attribute
    """
    # CRUD Routes

    This route contains the main methods that will be used to create, read, update and delete resources.

    todo: UPDATE THIS EXAMPLES TO MATCH THE NEW ROUTES...
    todo: Add the respective examples for each method
    ## Example
    - Create a new resource
    - Get all resources
    - Get a resource by ID
    - Update a resource by ID
    - Delete a resource by ID
    """

    views: APIRouter = APIRouter()  # todo: views routes... for views xd
    """
    # Views Routes

    This route contains the main methods that will be used to display the views of the application.

    ## Example
    - Get some useful view data to display on the application (for each schema)
    """

    print(f"\n\033[0;30;47mACADEMIC HUB\033[m\n")  # WHITE
    return home, basic_dt, crud_attr, views

home, basic_dt, crud_attr, views = define_routes()


# # * Some protected route...
# @home.get("/users/me", tags=["Auth"], response_model=UserResponse)
# def read_users_me(current_user: GeneralUser = Depends(get_current_user)):
#     return current_user

# * Authentication Routes (test routes) -------------------------------------------------------
# ^ This route is the only exception to be declared here.
# ^ This because it's the only route that will apply some kind of data manipulation.
# ^ This encrypts the password & stores it in the database, to avoid storing the password in plain text
@basic_dt.post("/general_user", tags=["GeneralUser"], response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(partial(get_db, "school"))):
    user_dict = user.model_dump()
    user_dict["password_hash"] = bcrypt_context.hash(user_dict["password_hash"])
    db_user = GeneralUser(**user_dict)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise e
    return db_user


def _add_schema_routes(
        schema: str, 
        schema_classes: list[Type[Base]],  # type: ignore
        db_dependency: Callable, 
        b_color: str = ""
    ):
    print(f"\033[0;30;{b_color}m{schema.capitalize()}\033[m")  # YELLOW
    # print(f"\033[0;30;{b_color}mACADEMIC HUB - {schema.capitalize()}\033[m")  # YELLOW
    for schema_class in schema_classes:
        print(f"    \033[3m{schema_class.__name__}\033[m")
        dt_routes(schema_class, UserResponse, basic_dt, db_dependency)
        # crud_routes(...)
        # views_routes(...)
    print()


# todo: Add the respective routes for each schema
_add_schema_routes("school", auth_classes, partial(get_db, "school"), "43")

crud_routes(
    model=GeneralUser,
    create_model=UserCreate,
    update_model=UserCreate,
    response_model=UserResponse,
    router=basic_dt,
    db_dependency=partial(get_db, "school")
)




# * views routes -----------------------------------------------------------------------------------------------
def _views_routes(
    router: APIRouter, 
    db_dependency: Callable,
):
    """
    Creates views routes for a given model and home.

    Args:
        router (APIRouter): The FastAPI router to which the endpoints will be added.
        db_dependency (Callable): Dependency that provides a DB session.
    """
    @home.get("/views/{view_name}/", tags=["views"])  # Decorate the route function with the GET route for getting all resources
    def get_view(view_name: str, db: Session = Depends(db_dependency)):  # Route function to get all resources
        view = db.execute(f"SELECT * FROM {view_name}").fetchall()  # Execute a raw SQL query to get the view data
        if not view:  # If the view is empty
            raise HTTPException(
                status_code=404,
                detail=f"No view named '{view_name}' found."
            )
        return view  # Return the view data

    # todo: SET THE AUTH FOR EACH USER (ADMIN or USER)
    # todo: ADMIN must be able to see all the tables for his schema (FOR EACH SCHEMA)
    # todo: USER can just see the data associated to him (school & library) 
